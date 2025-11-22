import SectionTitle from "@/components/section-title";
import { ExternalLinkIcon } from "lucide-react";

const steps = [
    {
        id: 1,
        title: "Define HR Requirements",
        description: "Start with your HR needs - recruitment, talent management, performance reviews, or compliance. TalentPilot's orchestration engine interprets your requirements and creates the workflow in seconds.",
        link: "https://prebuiltui.com/tailwind-templates",
        image: "/assets/workflow1.png",
    },
    {
        id: 2,
        title: "Customize & Configure",
        description: "Adjust recruitment pipelines, candidate assessments, and HR workflows. Configure data sources, set performance metrics, and integrate with your existing HR systems.",
        link: "https://prebuiltui.com/tailwind-templates",
        image: "/assets/workflow2.png",
    },
    {
        id: 3,
        title: "Deploy & Orchestrate",
        description: "Launch your HR orchestration and let TalentPilot run. It manages talent workflows autonomously, tracks analytics, and optimizes HR operations continuously.",
        link: "https://prebuiltui.com/tailwind-templates",
        image: "/assets/workflow3.png",
    },
];

export default function WorkflowSteps() {
    return (
        <section className="mt-32 relative">
            <SectionTitle
                title="From HR Strategy to Automated Orchestration Quickly and Effortlessly."
                description="Transform your HR operations with AI-powered orchestration that optimizes talent management and accelerates performance."
            />

            <div className="relative space-y-20 md:space-y-30 mt-20">
                <div className="flex-col items-center hidden md:flex absolute left-1/2 -translate-x-1/2">
                    <p className="flex items-center justify-center font-medium my-10 aspect-square bg-black/15 p-2 rounded-full">
                        01
                    </p>
                    <div className="h-72 w-0.5 bg-gradient-to-b from-transparent via-white to-transparent" />
                    <p className="flex items-center justify-center font-medium my-10 aspect-square bg-black/15 p-2 rounded-full">
                        02
                    </p>
                    <div className="h-72 w-0.5 bg-gradient-to-b from-transparent via-white to-transparent" />
                    <p className="flex items-center justify-center font-medium my-10 aspect-square bg-black/15 p-2 rounded-full">
                        03
                    </p>
                </div>
                {steps.map((step, index) => (
                    <div key={index} className={`flex items-center justify-center gap-6 md:gap-20 ${index % 2 !== 0 ? 'flex-col md:flex-row-reverse' : 'flex-col md:flex-row'}`}>
                        <img src={step.image} alt="step" className="flex-1 h-auto w-full max-w-sm rounded-2xl" />
                        <div key={index} className="flex-1 flex flex-col gap-6 md:px-6 max-w-md">
                            <h3 className="text-2xl font-medium text-white">
                                {step.title}
                            </h3>
                            <p className="text-gray-100 text-sm/6 line-clamp-3 pb-2">
                                {step.description}
                            </p>
                            <a href={step.link} className="flex items-center gap-2">
                                Learn More
                                <ExternalLinkIcon className="size-4" />
                            </a>
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
}
