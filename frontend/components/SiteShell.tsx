"use client";
import Link from "next/link";
import { BookOpen, ChartNoAxesCombined, LayoutDashboard, Mic2, Sparkles } from "lucide-react";
import { usePathname } from "next/navigation";
const links = [{ href: "/dashboard", label: "Overview", icon: LayoutDashboard }, { href: "/lessons", label: "Lessons", icon: BookOpen }, { href: "/practice", label: "Practice", icon: Mic2 }, { href: "/progress", label: "Progress", icon: ChartNoAxesCombined }];
export function Brand() { return <Link className="brand" href="/"><span className="brand-mark"><Sparkles size={17}/></span>verba</Link>; }
export default function SiteShell({ children }: {children: React.ReactNode}) { const path = usePathname(); return <div className="app-shell"><aside className="side"><Brand/><nav>{links.map(({href,label,icon:Icon})=><Link key={href} className={path===href ? "nav active" : "nav"} href={href}><Icon size={18}/>{label}</Link>)}</nav><div className="side-note"><span>STREAK</span><strong>12 days</strong><p>Keep your rhythm going.</p></div><div className="user"><div className="avatar">MA</div><div><b>Marisa Adeyemi</b><small>Teacher</small></div></div></aside><main className="app-main">{children}</main><nav className="mobile-nav">{links.map(({href,label,icon:Icon})=><Link key={href} className={path===href ? "active" : ""} href={href}><Icon size={19}/><span>{label}</span></Link>)}</nav></div>; }
