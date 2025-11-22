import { Poppins } from 'next/font/google';
import './globals.css';
import LenisScroll from '@/components/lenis-scroll';

const poppins = Poppins({
    subsets: ['latin'],
    variable: '--font-sans',
    weight: ['400', '500', '600', '700'],
});

export default function RootLayout({ children }) {
    return (
        <html lang='en'>
            <LenisScroll />
            <body>{children}</body>
        </html>
    );
}
