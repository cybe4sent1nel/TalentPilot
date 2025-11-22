import ChatScrollHandler from '@/components/chat-scroll-handler';

export default function ChatLayout({ children }) {
    return (
        <>
            <ChatScrollHandler />
            <div className='fixed inset-0 overflow-hidden -z-20 pointer-events-none'>
                <div className='absolute rounded-full top-80 left-1/3 -translate-x-1/2 size-130 bg-[#D10A8A] blur-[100px]' />
                <div className='absolute rounded-full top-80 -right-20 -translate-x-1/2 size-130 bg-[#2E08CF] blur-[100px]' />
                <div className='absolute rounded-full top-0 left-1/2 -translate-x-1/2 size-130 bg-[#F26A06] blur-[100px]' />
            </div>
            <div className='flex h-screen flex-col'>
                {children}
            </div>
        </>
    );
}
