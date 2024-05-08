import os
from minio import Minio
from minio.error import S3Error
from datetime import timedelta
from minio.deleteobjects import DeleteObject
from qiniu import Auth, put_file, BucketManager
import hashlib
import datetime


class QiniuOss(object):
    auth = None
    policy = '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetBucketLocation","s3:ListBucket"],"Resource":["arn:aws:s3:::%s"]},{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetObject"],"Resource":["arn:aws:s3:::%s/*"]}]}'

    def __new__(cls, *args, **kwargs):
        if not cls.auth:
            cls.auth = object.__new__(cls)
        return cls.auth

    def __init__(self, access_key, secret_key):
        self.auth = Auth(access_key,secret_key)

    def download_file(self, bucket_name, file, file_path, stream=1024*32):
        """
        Download file and write to local path
        :return:
        """
        # try:
        #     data = self.client.get_object(bucket_name, file)
        #     with open(file_path, "wb") as fp:
        #         for d in data.stream(stream):
        #             fp.write(d)
        # except S3Error as e:
        #     print("[error]:", e)

    def fget_file(self, bucket_name, file, file_path):
        """
        download file to local path
        :param file:
        :param file_path:
        :return:
        """
        self.client.fget_object(bucket_name, file, file_path)

    def copy_file(self, bucket_name, file, file_path):
        """
        copy file
        :param bucket_name:
        :param file:
        :param file_path:
        :return:
        """
        # self.client.copy_object(bucket_name, file, file_path)

    def fput_file(self, bucket_name, file, file_path):
        """
        write file to bucket
        :param file_path: local file path
        :param file: file name
        :return:
        """
        # 保存到本地临时文件
        # local_path = os.path.dirname(os.path.abspath(__file__))
        # localfile = os.path.join(local_path, file)
        localfile = file
        print(localfile)

        # 上传到七牛云的文件路径
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        file_path += "/" + year + "/" + month + "/"
        # 重命名文件

        key = self.md5_file(localfile)
        suffix = file.split(".")[-1]
        filename = key+'.'+suffix
        key = file_path + filename

        # 七牛云token
        token = self.auth.upload_token(bucket_name, key)

        put_file(token, key, localfile, version='v2')

        return 'https://cdn.metaagent.studio/'+key

    def stat_object(self, bucket_name, file_path):
        """
        Get meta data of an object
        :param bucket_name:
        :param file:
        :return:
        """
        # try:
        #初始化BucketManager
        bucket = BucketManager(self.auth)

        ret, data = bucket.stat(bucket_name, file_path)
        print(data.bucket_name)
        print(data.object_name)
        print(data.last_modified)
        print(data.etag)
        print(data.size)
        print(data.metadata)
        print(data.content_type)
        # except S3Error as e:
        #     print("[error]:", e)

    def remove_file(self, bucket_name, file):
        """
        Remove single file
        :return:
        """
        self.client.remove_object(bucket_name, file)

    def remove_files(self, bucket_name, file_list):
        """
        remove files
        :return:
        """
        delete_object_list = [DeleteObject(file) for file in file_list]
        for del_err in self.client.remove_objects(bucket_name, delete_object_list):
            print("del_err", del_err)

    def presigned_get_file(self, bucket_name, file, days=7):
        """
        Generate a http URL
        :return:
        """
        return self.client.presigned_get_object(bucket_name, file, expires=timedelta(days=days))

    def md5_file(self, file_path):
        with open(file_path, 'rb') as file:
            block_size = 4096  # 每块的大小，可根据需求调整
            md5 = hashlib.md5()

            while True:
                block = file.read(block_size)
                if not block:
                    break
                md5.update(block)

            md5_code = md5.hexdigest()
            return md5_code


QINIU_OBJ = QiniuOss(access_key="yJD8wkxUhoYhtqMfdwXPJMLmdsgMaYlljBAkxdU0", secret_key="1iA9bp5athxixUaW-_e7TQEZTD-5a7aHYc32t7q4")