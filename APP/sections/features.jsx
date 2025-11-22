import SectionTitle from "@/components/section-title";
import { UsersIcon, TargetIcon, ZapIcon } from "lucide-react";

export default function Features() {

    const featuresData = [
        {
            icon: UsersIcon,
            title: "Talent Orchestration",
            description: "Automate recruitment, onboarding, and talent management across your organization.",
        },
        {
            icon: TargetIcon,
            title: "Strategic Insights",
            description: "Get AI-powered insights on talent gaps, performance trends, and HR analytics.",
        },
        {
            icon: ZapIcon,
            title: "Real-time Automation",
            description: "Orchestrate HR workflows instantly with seamless integration across systems.",
        }
    ];
    return (
        <section className="mt-32">
            <SectionTitle
                title="TalentPilot Orchestration Capabilities"
                description="Intelligent HR operations powered by IBM WatsonX for modern talent management."
            />
            <div className="flex flex-wrap items-center justify-center gap-6 mt-10 px-6">
                {featuresData.map((feature, index) => (
                    <div key={index} className="hover:-translate-y-0.5 transition duration-300 p-6 rounded-xl space-y-4 glass max-w-80 w-full">
                        <feature.icon className="size-8.5" />
                        <h3 className="text-base font-medium text-white">
                            {feature.title}
                        </h3>
                        <p className="text-gray-100 line-clamp-2 pb-2">
                            {feature.description}
                        </p>
                    </div>
                ))}
            </div>
        </section>
    )
}