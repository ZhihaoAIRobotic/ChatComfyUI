import Messages from "components/messages";
import PromptForm from "components/prompt-form";
import PromptVideoForm from "components/prompt_video-form";
import Head from "next/head";
import { useEffect, useState } from "react";
// import ReactPlayer from "react-player";
import Footer from "components/footer";
import Link from 'next/link';
import Image from 'next/image'
import { useRouter } from 'next/router';

import prepareImageFileForUpload from "lib/prepare-image-file-for-upload";
import { getRandomSeed } from "lib/seeds";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export const appName = "ChatComfyUI";
export const appSubtitle = "Generate your own artwork, with the help of ChatComfyUI.";
export const appMetaDescription = "Generate your own artwork, with the help of ChatComfyUI.";

export default function Home() {
  const [events, setEvents] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [error, setError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [seed] = useState(getRandomSeed());
  const [initialPrompt, setInitialPrompt] = useState(seed.prompt);

  // set the initial image from a random seed
  useEffect(() => {
    setEvents([{ image: seed.image}]);
  }, [seed.image]);

  const handleImageDropped = async (image) => {
    try {
      image = await prepareImageFileForUpload(image);
    } catch (error) {
      setError(error.message);
      return;
    }
    setEvents(events.concat([{ image }]));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const prompt = e.target.prompt.value;
    const lastImage = events.findLast((ev) => ev.image)?.image;

    setError(null);
    setIsProcessing(true);
    setInitialPrompt("");

    // make a copy so that the second call to setEvents here doesn't blow away the first. Why?
    const myEvents = [...events, { prompt }];
    setEvents(myEvents);

  };

  const startOver = async (e) => {
    e.preventDefault();
    setEvents(events.slice(0, 1));
    setError(null);
    setIsProcessing(false);
    setInitialPrompt(seed.prompt);
  };

  //  导航到子页面
  const router = useRouter();
  const handleItemClick = (itemId) => {
    router.push(`/agents/${itemId}`);
  };

  // agents列表
  const AgentLists = [
   { id: 1, router: 'text2img', title: 'Text2img Agent', desc: 'Your AI image generation Agent. It creates an image from scratch from a text description.', image: '/photo.svg' },
   { id: 2, router: 'img2img', title: 'Img2img Agent', desc: 'Your AI image translation Agent. It changes an image style according to a text description.', image: '/img.svg' },
   { id: 3, router: 'text2video', title: 'Text2video Agent', desc: 'Your AI video generation Agent. It creates an video clip from scratch from a text description.', image: '/video.svg'},
  ];

  const TitleStyle = {
    textAlign: 'center',
    background: 'linear-gradient(to right, #30cfd0, #330867)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    fontWeight: 'bold', color: 'red', fontSize: '32px',
  };
  
  const DescStyle = {
    textAlign: 'center',
    background: 'black',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    color: 'black', fontSize: '22px',
  };

  return (
    <div>
      <Head>
        <title>{appName}</title>
        <meta name="description" content={appMetaDescription} />
        <meta property="og:title" content={appName} />
        <meta property="og:description" content={appMetaDescription} />
        <meta property="og:image" content="https://paintbytext.chat/opengraph.jpg" />
      </Head>
      
      <main className="container max-w-[700px] mx-auto p-5">
        <hgroup>
          <h1 className="text-center text-5xl font-bold m-6">{appName}</h1>
          <p className="text-center text-xl opacity-60 m-6">
            {appSubtitle}
          </p>
        </hgroup>

    <div>
      <ul>
        {AgentLists.map((AgentLists) => (
          <li key={AgentLists.id} onClick={() => handleItemClick(AgentLists.router)} style={{ cursor: 'pointer' }}>
          <div style={{ borderRadius: '20px', backgroundColor: '#F4F5F7', width: '650px', height: '280px', 
          boxShadow: '10px 10px 10px 10px rgba(0, 0, 0.15, 0.15)', marginBottom: '40px', display: 'flex', justifyContent: 'space-around', alignItems: 'center'}}>
          <a>
          <div style={{ display: 'flex', justifyContent: 'center' }}>
          <Image src={AgentLists.image} width={120} height={240}/>
          </div>
            <span> <div style={TitleStyle}> {AgentLists.title}
            </div></span>
            <span> <div style={DescStyle}> {AgentLists.desc}          
            </div></span>
          </a>
          </div>
          </li>
        ))}
      </ul>
    </div>

      </main>
    </div>
  );
}