import SectionTitle from "@/components/section-title";

export default function Testimonials() {
    const data = [
        {
            review: 'TalentPilot has transformed our recruitment process. We reduced time-to-hire by 40% and improved candidate quality significantly.',
            name: 'Richard Nelson',
            about: 'HR Director, TechCorp',
            rating: 5,
            image: 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?q=80&w=200',
        },
        {
            review: 'The intelligence and automation of TalentPilot has made talent management effortless. Our entire team is more productive.',
            name: 'Sophia Martinez',
            about: 'Chief People Officer, StartupX',
            rating: 5,
            image: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=200',
        },
        {
            review: 'Outstanding orchestration capabilities. TalentPilot integrates seamlessly with our existing systems and delivers real results.',
            name: 'Ethan Roberts',
            about: 'VP Human Resources, Enterprise Co',
            rating: 5,
            image: 'https://images.unsplash.com/photo-1527980965255-d3b416303d12?w=200&auto=format&fit=crop&q=60',
        },
        {
            review: 'The insights from TalentPilot powered by IBM WatsonX have helped us make data-driven talent decisions like never before.',
            name: 'Isabella Kim',
            about: 'Talent Manager, Global Inc',
            rating: 5,
            image: 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=200&auto=format&fit=crop&q=60',
        },
        {
            review: "TalentPilot's automation capabilities freed up my team from repetitive tasks. We now focus on strategic talent initiatives.",
            name: 'Liam Johnson',
            about: 'HR Operations Manager, Digital Solutions',
            rating: 5,
            image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=100&h=100&auto=format&fit=crop',
        },
        {
            review: 'The AI-powered orchestration is remarkable. TalentPilot adapts to our unique HR workflows perfectly.',
            name: 'Ava Patel',
            about: 'HR Executive, Growth Ventures',
            rating: 5,
            image: 'https://raw.githubusercontent.com/prebuiltui/prebuiltui/main/assets/userImage/userImage1.png',
        },
    ];
    return (
        <section className="mt-32 flex flex-col items-center">
            <SectionTitle
                title="What HR Leaders Say About TalentPilot"
                description="See how TalentPilot is revolutionizing HR operations and talent management across organizations."
            />
            <div className='mt-12 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3'>
                {data.map((item, index) => (
                    <div key={index} className='w-full max-w-88 space-y-5 rounded-lg glass p-5 transition-all duration-300 hover:-translate-y-1'>
                        <div className='flex items-center justify-between'>
                            <p className="font-medium">{item.about}</p>
                            <img className='size-10 rounded-full' src={item.image} alt={item.name} />
                        </div>
                        <p className='line-clamp-3'>“{item.review}”</p>
                        <p className='text-gray-300'>
                            - {item.name}
                        </p>
                    </div>
                ))}
            </div>
        </section>
    );
}