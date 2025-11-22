import { GithubIcon, LinkedinIcon, TwitterIcon } from "lucide-react";
import Link from "next/link";

export default function Footer() {
    const links = [
        { name: 'Terms of Service', href: '#terms-of-service' },
        { name: 'Privacy Policy', href: '#privacy-policy' },
        { name: 'Security', href: '#security' },
        { name: 'Sitemap', href: '#sitemap' },
    ];
    return (
        <footer className="flex flex-col items-center px-4 md:px-16 lg:px-24 justify-center w-full pt-16 mt-40 glass border-0">
            <h2 className='text-2xl font-bold'>TalentPilot</h2>
            <p className="text-sm text-gray-400 mt-1">Powered by IBM WatsonX</p>

            <div className="flex flex-wrap items-center justify-center gap-8 py-8">
                {links.map((link, index) => (
                    <Link key={index} href={link.href} className='transition hover:text-gray-300'>
                        {link.name}
                    </Link>
                ))}
            </div>
            <div className="flex items-center gap-6 pb-6">
                <a href="#" className="hover:-translate-y-0.5 text-gray-200 transition-all duration-300">
                    <LinkedinIcon />
                </a>
                <a href="#" className="hover:-translate-y-0.5 text-gray-200 transition-all duration-300">
                    <TwitterIcon />
                </a>
                <a href="#" className="hover:-translate-y-0.5 text-gray-200 transition-all duration-300">
                    <GithubIcon />
                </a>
            </div>
            <hr className="w-full border-white/20 mt-6" />
            <div className="flex flex-col md:flex-row items-center w-full justify-between gap-4 py-4">
                <p>Intelligent HR Orchestration</p>
                <p>Designed and developed by Fahad Khan. Copyright © 2025 TalentPilot. All rights reserved.</p>
            </div>
        </footer>
    );
};