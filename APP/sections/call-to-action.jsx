import { ArrowRightIcon, BrainIcon, BarChart3Icon, UsersIcon } from "lucide-react";
import Link from "next/link";

export default function CallToAction() {
    const features = [
        {
            icon: <BrainIcon className="size-6" />,
            title: "AI-Powered Intelligence",
            description: "Leverage IBM WatsonX for advanced HR analytics and insights"
        },
        {
            icon: <BarChart3Icon className="size-6" />,
            title: "Real-time Analytics",
            description: "Track recruitment, engagement, and training metrics instantly"
        },
        {
            icon: <UsersIcon className="size-6" />,
            title: "Talent Management",
            description: "Optimize your recruitment and employee development strategies"
        }
    ];

    return (
        <div className="flex flex-col max-w-5xl mt-40 mx-auto items-center justify-center text-center py-16 rounded-xl">
            <div className="glass p-12 rounded-xl">
                <h2 className="text-2xl md:text-4xl font-medium mt-2">
                    Ready to Transform Your HR with TalentPilot?
                </h2>
                <p className="mt-4 text-sm/7 max-w-md mx-auto text-gray-300">
                    See how fast you can turn your ideas into reality. Get started for free, no credit card required.
                </p>

                {/* TalentPilot Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-10 mb-8">
                    {features.map((feature, idx) => (
                        <div key={idx} className="flex flex-col items-center p-4">
                            <div className="text-[#D10A8A] mb-3">
                                {feature.icon}
                            </div>
                            <h3 className="font-semibold text-sm mb-2">{feature.title}</h3>
                            <p className="text-xs text-gray-400">{feature.description}</p>
                        </div>
                    ))}
                </div>

                <Link href="/chat" className="btn glass flex items-center gap-2 mt-8 mx-auto">
                    Start Using TalentPilot
                    <ArrowRightIcon className="size-4" />
                </Link>
            </div>
        </div>
    );
};