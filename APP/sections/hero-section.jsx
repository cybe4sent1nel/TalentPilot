import { PlayCircleIcon } from "lucide-react";
import Link from "next/link";

export default function HeroSection() {

    return (
        <section className="flex flex-col items-center">
            <div className="flex items-center gap-3 mt-32">
                <p>Intelligent HR Orchestration Powered by IBM WatsonX</p>
                <button className="btn glass py-1 px-3 text-xs">
                    Launch App
                </button>
            </div>
            <h1 className="text-center text-4xl/13 md:text-6xl/19 mt-4 font-semibold tracking-tight max-w-3xl">
                TalentPilot: Your HR Intelligence Agent
            </h1>
            <p className="text-center text-gray-100 text-base/7 max-w-md mt-6">
                Automate recruitment, talent management, and HR operations with AI-powered orchestration. Designed and developed by Fahad Khan.
            </p>

            <div className="flex flex-col md:flex-row max-md:w-full items-center gap-4 md:gap-3 mt-6">
                <Link href="/chat" className="btn max-md:w-full glass py-3">
                    Start Chat
                </Link>
                <button className="btn max-md:w-full glass flex items-center justify-center gap-2 py-3">
                    <PlayCircleIcon className="size-4.5" />
                    Watch Demo
                </button>
            </div>
        </section >
    );
}