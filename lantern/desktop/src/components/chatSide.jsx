import send from '../assets/send.svg'
import { useEffect, useRef } from 'react';

function ReceivedMessage({ message }) {
    return (
        <div className="flex">
            <div className="px-3 py-2 bg-accent-color w-fit rounded-xl rounded-tl-none mr-5">
                <h1>{message}</h1>
            </div>
        </div>
    )
}

function SentMessage({ message }) {
    return (
        <div className="flex justify-end">
            <div className="px-3 py-2 bg-secondary-color w-fit rounded-xl rounded-tr-none ml-5">
                <h1>{message}</h1>
            </div>
        </div>
    )
}

function ChatBar() {
    return (
        <div className="flex justify-between items-center outline outline-2 outline-secondary-color rounded-lg p-3 mt-3">
            <span><span className="text-accent-color font-bold">~/Arundas $</span> Hello bro! Coorg varunnundo?</span>
            <img src={send} alt="send" />
        </div>
    )
}

function ChatSide() {
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    });

    return (
      <div className="flex flex-col flex-2 h-full bg-primary-color p-5">
        <div id="chat-body" className="flex flex-col gap-2 flex-1 overflow-y-auto">
          <SentMessage message="Hey! Are you free to chat?" />
          <ReceivedMessage message="Yeah, just finished my work. What's up?" />
          <SentMessage message="I was thinking about that project we discussed last week" />
          <ReceivedMessage message="Oh the file sharing app? How's it going?" />
          <SentMessage message="Pretty well actually! I got the CLI version working perfectly. You can share files between devices on the same network without any issues." />
          <ReceivedMessage message="That's awesome! I remember you were struggling with the network discovery part. Did you figure that out?" />
          <SentMessage message="Yeah, I ended up using UDP broadcasting for device discovery and then establishing TCP connections for the actual file transfer. It's much more reliable now." />
          <ReceivedMessage message="Nice! That sounds like a solid approach. Are you planning to add any security features?" />
          <SentMessage message="Definitely! I'm thinking of adding encryption for the file transfers and maybe some kind of authentication system so only authorized devices can connect." />
          <ReceivedMessage message="Smart thinking. You don't want random people on the network accessing your files 😅" />
          <SentMessage message="Exactly! Speaking of which, I'm now working on a desktop GUI for it using Electron" />
          <ReceivedMessage message="Ooh fancy! Moving from CLI to GUI is a big step. How are you finding Electron?" />
          <SentMessage message="It's been interesting. I'm using React with Vite for the frontend, which makes development pretty smooth. The hardest part is figuring out how to integrate the existing CLI functionality with the Electron main process." />
          <ReceivedMessage message="Yeah, that IPC stuff can be tricky. Are you planning to keep both versions or eventually phase out the CLI?" />
          <SentMessage message="I think I'll keep both. The CLI is great for power users and automation, while the GUI will make it accessible to everyone else. Different tools for different use cases, you know?" />
          <ReceivedMessage message="Makes total sense. Plus having both gives users options, which is always good" />
          <SentMessage message="The design is coming along nicely too. I went for a clean, modern look with a dark theme" />
          <ReceivedMessage message="Can't go wrong with dark themes these days 😎" />
          <SentMessage message="Haha true! Everyone expects it now. Anyway, I should probably get back to coding. This chat interface isn't going to build itself!" />
          <ReceivedMessage message="Good luck with it! Let me know when you have a beta version ready. I'd love to test it out" />
          <SentMessage message="Will do! Thanks for listening to me ramble about code stuff 😅" />
          <ReceivedMessage message="Anytime! That's what friends are for. Catch you later!" />
          <SentMessage message="See ya! 👋" />
          <div ref={messagesEndRef} />
        </div>
        <ChatBar />
      </div>
    )
}
export default ChatSide;