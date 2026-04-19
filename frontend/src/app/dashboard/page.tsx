"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bookmark, CheckCircle, Search, ShieldCheck, Activity, X, ArrowRight, UploadCloud, Building2, Briefcase, HeartPulse, GraduationCap, Coins, Zap, Layers } from "lucide-react";
import Link from "next/link";

export default function Dashboard() {
  const [activeCategory, setActiveCategory] = useState("All");
  const [isVerifying, setIsVerifying] = useState(true);
  const [selectedScheme, setSelectedScheme] = useState<any>(null);
  
  const [appliedSchemes, setAppliedSchemes] = useState<number[]>([]);
  const [isApplying, setIsApplying] = useState(false);
  const [uploading, setUploading] = useState(false);

  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      setMousePosition({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      });
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => setIsVerifying(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  const allSchemes = [
    { id: 1, name: "Pradhan Mantri Awas Yojana", department: "Ministry of Housing", matchingScore: "98%", status: "Eligible", category: "Housing", description: "Credit-linked subsidies for purchasing/building homes.", benefits: "Up to ₹2.67L interest subsidy", howToApply: ["Visit official portal", "Select Citizen Assessment"], docs: ["Aadhaar", "PAN"] },
    { id: 13, name: "DDA Housing Scheme", department: "Delhi Dev Authority", matchingScore: "81%", status: "Review Required", category: "Housing", description: "Allotment of flats for EWS, LIG, MIG.", benefits: "Subsidized home allocations via lottery", howToApply: ["Register online", "Pay booking"], docs: ["Aadhaar", "Bank Details"] },
    { id: 2, name: "Ayushman Bharat PM-JAY", department: "Ministry of Health", matchingScore: "95%", status: "Eligible", category: "Healthcare", description: "Health insurance scheme fully financed by government.", benefits: "Cashless healthcare of ₹5 Lakhs", howToApply: ["Check eligibility online", "Verify identity"], docs: ["Aadhaar Card", "Ration Card"] },
    { id: 8, name: "Janani Suraksha Yojana", department: "National Health Mission", matchingScore: "89%", status: "Eligible", category: "Healthcare", description: "Safe motherhood intervention for pregnant women.", benefits: "Cash assistance during delivery", howToApply: ["Contact local ASHA", "Register"], docs: ["Aadhaar", "Bank Account"] },
    { id: 3, name: "PM-KISAN Samman Nidhi", department: "Ministry of Agriculture", matchingScore: "88%", status: "Review Required", category: "Agriculture", description: "Support scheme wherein small farmers get ₹6,000 per year.", benefits: "₹2,000 transferred every 4 months", howToApply: ["Go to official website", "Upload land documents"], docs: ["Aadhaar", "Land Records"] },
    { id: 10, name: "PM Fasal Bima Yojana", department: "Ministry of Agriculture", matchingScore: "84%", status: "Eligible", category: "Agriculture", description: "Crop insurance policy against natural calamities.", benefits: "Financial support against crop failure", howToApply: ["Apply via bank branch", "Or online"], docs: ["Aadhaar", "Sowing Cert"] },
    { id: 4, name: "Sukanya Samriddhi Yojana", department: "Ministry of Women", matchingScore: "92%", status: "Eligible", category: "Education", description: "Deposit scheme for girl child with tax benefits.", benefits: "High interest rate 8.2%", howToApply: ["Visit Post Office", "Submit certificates"], docs: ["Child's Birth Cert", "Guardian ID"] },
    { id: 11, name: "National Scholarship Portal", department: "Ministry of Education", matchingScore: "94%", status: "Eligible", category: "Education", description: "One-stop portal for all govt scholarships.", benefits: "Direct scholarship via DBT", howToApply: ["Register on NSP", "Upload marks"], docs: ["Aadhaar", "Marksheets"] },
    { id: 5, name: "Atal Pension Yojana (APY)", department: "Ministry of Finance", matchingScore: "85%", status: "Action Needed", category: "Financial", description: "Pension scheme for unorganized sector.", benefits: "Guaranteed pension of ₹1k-₹5k", howToApply: ["Approach bank branch", "Setup auto-debit"], docs: ["Bank Account", "Aadhaar"] },
    { id: 6, name: "MUDRA Yojana", department: "Ministry of Finance", matchingScore: "78%", status: "Review Required", category: "Business", description: "Provides loans up to 10 lakh to micro enterprises.", benefits: "Collateral-free loans", howToApply: ["Submit loan application to Bank", "Provide business plan"], docs: ["ID Proof", "Quotation"] },
    { id: 12, name: "Stand-Up India", department: "Ministry of Finance", matchingScore: "88%", status: "Eligible", category: "Business", description: "Facilitates bank loans for SC/ST and women entrepreneurs.", benefits: "Bank loans 10 lakh to 1 Cr", howToApply: ["Apply via SIDBI portal", "At District Manager"], docs: ["Aadhaar", "Project Report"] }
  ];

  const categories = [
    { name: "All", icon: <Layers className="w-4 h-4" /> },
    { name: "Housing", icon: <Building2 className="w-4 h-4" /> },
    { name: "Healthcare", icon: <HeartPulse className="w-4 h-4" /> },
    { name: "Agriculture", icon: <Activity className="w-4 h-4" /> },
    { name: "Education", icon: <GraduationCap className="w-4 h-4" /> },
    { name: "Business", icon: <Briefcase className="w-4 h-4" /> },
    { name: "Financial", icon: <Coins className="w-4 h-4" /> },
  ];

  const filteredSchemes = activeCategory === "All" ? allSchemes : allSchemes.filter(s => s.category === activeCategory);

  useEffect(() => {
    if (selectedScheme) document.body.style.overflow = 'hidden';
    else { document.body.style.overflow = 'unset'; setIsApplying(false); }
  }, [selectedScheme]);

  // VITAL missing Handle Upload fix here
  const handleUploadSubmit = () => {
    setUploading(true);
    setTimeout(() => {
      setUploading(false);
      setIsApplying(false);
      if(selectedScheme) {
        setAppliedSchemes([...appliedSchemes, selectedScheme.id]);
      }
    }, 2500);
  };

  return (
    <div 
      ref={containerRef} onMouseMove={handleMouseMove}
      className="min-h-screen bg-[#020204] flex flex-col md:flex-row font-sans selection:bg-blue-500/30 relative text-white overflow-hidden"
    >
      <motion.div
        className="pointer-events-none absolute inset-0 z-0 transition-opacity duration-300 mix-blend-screen"
        animate={{
          background: `radial-gradient(800px circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(59, 130, 246, 0.15), transparent 40%)`
        }}
      />
      <div className="absolute inset-0 bg-mesh opacity-60 z-0 pointer-events-none" />
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10 pointer-events-none z-0 mix-blend-overlay" />

      {/* Midnight Neon Sidebar */}
      <aside className="w-full md:w-72 bg-[#05050A]/60 backdrop-blur-3xl border-r border-white/5 p-8 flex flex-col justify-between z-20 shadow-2xl relative">
        <div className="absolute top-0 right-0 w-px h-full bg-gradient-to-b from-transparent via-blue-500/30 to-transparent" />
        <div>
          <div className="flex items-center gap-3 mb-16">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-600 to-fuchsia-600 flex items-center justify-center text-white font-black shadow-[0_0_30px_rgba(59,130,246,0.6)]">GS</div>
            <span className="text-3xl font-black tracking-tight text-white">Gov<span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-fuchsia-400">Scheme</span></span>
          </div>
          
          <div className="mb-12 p-6 rounded-3xl bg-black/60 border border-white/10 relative overflow-hidden shadow-[0_0_40px_rgba(0,0,0,0.8)] backdrop-blur-md">
            <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-blue-500 via-fuchsia-500 to-blue-500 opacity-60 animate-pulse" />
            <h3 className="text-slate-400 text-xs font-bold uppercase tracking-widest mb-3">AI Verification</h3>
            <div className="flex items-end gap-2 mb-4">
              <span className="text-5xl font-extrabold text-white">85</span>
              <span className="text-blue-500 mb-1 font-black text-xl">%</span>
            </div>
            <div className="w-full bg-black/80 rounded-full h-2.5 overflow-hidden border border-white/5">
              <motion.div initial={{ width: 0 }} animate={{ width: "85%" }} transition={{ duration: 1.5 }} className="bg-gradient-to-r from-blue-500 to-fuchsia-500 h-full rounded-full shadow-[0_0_15px_rgba(59,130,246,0.9)]" />
            </div>
            <p className="text-xs text-blue-400 font-bold mt-5 flex items-center gap-2"><ShieldCheck className="w-4 h-4" /> Vector Matched</p>
          </div>

          <nav className="space-y-4">
            <Link href="/dashboard" className="flex items-center gap-3 px-5 py-4 bg-gradient-to-r from-blue-500/10 to-transparent border border-blue-500/20 text-blue-400 rounded-2xl font-bold shadow-[inset_0_0_20px_rgba(59,130,246,0.1)]">
              <Bookmark className="w-5 h-5 flex-shrink-0" /> Database Explorer
            </Link>
            <Link href="/chat" className="flex items-center gap-3 px-5 py-4 text-slate-400 hover:bg-white/5 hover:text-white rounded-2xl font-bold border border-transparent hover:border-white/10 group">
              <span className="w-5 h-5 flex items-center justify-center flex-shrink-0 group-hover:text-fuchsia-400 transition-colors">💬</span> AI Copilot
            </Link>
          </nav>
        </div>
      </aside>

      {/* Main Panel */}
      <main className="flex-1 relative overflow-hidden h-screen overflow-y-auto no-scrollbar z-10">
        <div className="p-6 md:p-12">
          <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-6 border-b border-white/5 pb-8 relative">
            <div>
              <div className="flex items-center gap-4 mb-3">
                <h1 className="text-4xl md:text-5xl font-black text-white tracking-tight drop-shadow-2xl">Scheme Matrix</h1>
                {isVerifying ? (
                  <span className="px-4 py-1.5 bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 text-[10px] font-black uppercase tracking-widest rounded-full flex items-center gap-2 animate-pulse backdrop-blur-xl">
                     <span className="w-2 h-2 rounded-full bg-yellow-400 animate-ping"/> Analyzing...
                  </span>
                ) : (
                  <motion.span initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} className="px-4 py-1.5 bg-blue-500/10 border border-blue-500/30 text-blue-400 text-[10px] font-black uppercase tracking-widest rounded-full flex items-center gap-2 backdrop-blur-xl shadow-[0_0_20px_rgba(59,130,246,0.2)]">
                     <Zap className="w-3 h-3 text-fuchsia-400" /> Live Render
                  </motion.span>
                )}
              </div>
              <p className="text-slate-400 font-medium text-lg">Securely filtering <span className="text-white">12,402</span> government endpoints.</p>
            </div>
            
            <div className="relative w-full md:w-80 group">
                <Search className="w-5 h-5 text-slate-500 absolute left-4 top-1/2 -translate-y-1/2 group-focus-within:text-blue-400 transition-colors" />
                <input type="text" placeholder="Search protocol..." className="bg-[#05050A]/80 border border-white/10 text-sm rounded-full pl-12 pr-4 py-4 text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 w-full transition-all shadow-[inset_0_0_20px_rgba(0,0,0,0.5)] backdrop-blur-xl" />
            </div>
          </header>

          <div className="flex overflow-x-auto pb-4 mb-8 gap-3 no-scrollbar items-center">
            {categories.map((cat) => (
              <button 
                key={cat.name} onClick={() => setActiveCategory(cat.name)} 
                className={`flex items-center gap-2 px-6 py-4 rounded-2xl text-sm font-bold whitespace-nowrap transition-all border ${activeCategory === cat.name ? 'bg-blue-600 border-blue-500 text-white shadow-[0_0_30px_rgba(59,130,246,0.4)]' : 'bg-black/40 border-white/5 text-slate-400 hover:text-white hover:bg-white/5 backdrop-blur-xl'}`}
              >
                {cat.icon} {cat.name}
              </button>
            ))}
          </div>

          <motion.div layout className="grid xl:grid-cols-3 md:grid-cols-2 gap-6 pb-32">
            <AnimatePresence mode="popLayout">
              {filteredSchemes.map((scheme, i) => {
                const isStatusApplied = appliedSchemes.includes(scheme.id);
                return (
                <motion.div
                  layout initial={{ opacity: 0, scale: 0.9, y: 30 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.9 }} transition={{ delay: isVerifying ? i * 0.1 : i * 0.05, ease: [0.23, 1, 0.32, 1] }} key={scheme.id} onClick={() => setSelectedScheme(scheme)}
                  className="group cursor-pointer relative bg-gradient-to-b from-white/[0.03] to-transparent backdrop-blur-2xl border border-white/5 p-7 rounded-[2rem] hover:bg-white/[0.05] hover:border-blue-500/30 transition-all flex flex-col h-full hover:shadow-[0_20px_40px_-20px_rgba(59,130,246,0.3)] overflow-hidden"
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 via-transparent to-fuchsia-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
                  
                  <div className="flex justify-between items-start mb-6 relative z-10">
                    <span className="px-3 py-1 bg-black/60 border border-white/5 text-slate-300 text-[10px] font-bold rounded-lg tracking-widest uppercase shadow-inner">{scheme.category}</span>
                    {isStatusApplied ? (
                      <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center border border-green-500/40 shadow-[0_0_15px_rgba(34,197,94,0.3)]"><CheckCircle className="w-4 h-4 text-green-400" /></div>
                    ) : scheme.status === "Eligible" ? (
                      <span className="text-blue-400 text-[10px] font-black bg-blue-500/10 px-3 py-1.5 rounded-lg border border-blue-500/20 uppercase">Eligible</span>
                    ) : (
                      <span className="text-yellow-400 text-[10px] font-black bg-yellow-500/10 px-3 py-1.5 rounded-lg border border-yellow-500/20 uppercase">Review</span>
                    )}
                  </div>
                  
                  <h3 className="text-2xl font-black text-white mb-2 leading-tight group-hover:text-blue-400 transition-colors relative z-10 tracking-tight">{scheme.name}</h3>
                  <p className="text-fuchsia-400 text-xs font-black uppercase tracking-wider mb-4 relative z-10">{scheme.department}</p>
                  <p className="text-slate-400 text-sm mb-8 flex-1 relative z-10 line-clamp-3 leading-relaxed font-medium">{scheme.description}</p>
                  
                  <div className="flex items-center justify-between mt-auto pt-6 border-t border-white/5 relative z-10">
                    <div>
                      <p className="text-[9px] text-slate-500 uppercase tracking-widest font-black mb-1">AI Confidence</p>
                      <p className="text-white font-black text-xl">{scheme.matchingScore}</p>
                    </div>
                    {isStatusApplied ? (
                      <span className="px-4 py-2 bg-green-500/10 text-green-400 text-xs font-black uppercase rounded-xl border border-green-500/20 shadow-[0_0_15px_rgba(34,197,94,0.2)]">Transmitted</span>
                    ) : (
                      <button className="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-white group-hover:bg-blue-600 group-hover:text-white transition-colors shadow-lg border border-white/10 group-hover:border-blue-500"><ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" /></button>
                    )}
                  </div>
                </motion.div>
                );
              })}
            </AnimatePresence>
          </motion.div>
        </div>
      </main>

      <AnimatePresence>
        {selectedScheme && (
          <>
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={() => setSelectedScheme(null)} className="fixed inset-0 bg-[#020204]/90 backdrop-blur-xl z-40" />
            <motion.div 
              initial={{ opacity: 0, x: "100%", scale: 0.95 }} animate={{ opacity: 1, x: 0, scale: 1 }} exit={{ opacity: 0, x: "100%" }} transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="fixed top-0 right-0 w-full md:w-[650px] h-full bg-[#05050A]/95 backdrop-blur-3xl border-l border-white/5 shadow-[0_0_100px_rgba(0,0,0,0.8)] z-50 overflow-y-auto no-scrollbar"
            >
              <div className="absolute top-0 right-0 w-full h-[300px] bg-gradient-to-b from-blue-600/10 to-transparent pointer-events-none" />
              <div className="p-10 relative z-10">
                <button onClick={() => setSelectedScheme(null)} className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/10 transition-colors mb-8 border border-white/5 backdrop-blur-xl shrink-0"><X className="w-5 h-5" /></button>

                <h2 className="text-4xl font-black text-white mb-3 tracking-tighter">{selectedScheme.name}</h2>
                <p className="text-fuchsia-400 font-bold text-lg mb-10 tracking-wide">{selectedScheme.department}</p>

                {appliedSchemes.includes(selectedScheme.id) ? (
                  <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="bg-green-500/10 border border-green-500/20 rounded-[2rem] p-10 text-center flex flex-col items-center justify-center mt-10 backdrop-blur-xl shadow-[0_0_50px_rgba(34,197,94,0.1)]">
                    <div className="w-24 h-24 bg-green-500/20 rounded-full flex items-center justify-center mb-8 shadow-[0_0_30px_rgba(34,197,94,0.3)]"><CheckCircle className="w-12 h-12 text-green-400" /></div>
                    <h3 className="text-3xl font-black text-white mb-3">Protocol Confirmed</h3>
                    <p className="text-green-400 font-medium text-lg">Your data was hashed and transmitted securely via AI core.</p>
                    <div className="mt-8 px-6 py-3 bg-black/50 rounded-xl border border-white/5 inline-block"><p className="text-slate-400 text-sm font-mono tracking-widest">TRACE_ID: GS-{Math.floor(Math.random()*1000000)}</p></div>
                  </motion.div>
                ) : isApplying ? (
                  <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-black/50 border border-white/5 rounded-[2rem] p-10 shadow-2xl backdrop-blur-md">
                    <h3 className="text-2xl font-black text-white mb-6 flex items-center gap-3"><UploadCloud className="w-7 h-7 text-blue-500"/> Express Pipeline</h3>
                    <p className="text-slate-400 text-base mb-8">Securely encode the required encrypted payloads to pipeline context.</p>
                    
                    <div className="space-y-4 mb-10">
                      {selectedScheme.docs.map((doc: string, idx: number) => (
                        <div key={idx} className="relative group cursor-pointer">
                          <input type="file" className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
                          <div className="flex items-center justify-between p-5 bg-white/5 border border-white/5 rounded-2xl group-hover:border-blue-500/50 transition-all bg-gradient-to-r hover:from-blue-500/10 hover:to-transparent">
                            <span className="text-slate-200 font-bold text-base tracking-wide">{doc}</span>
                            <span className="text-xs font-black bg-white/5 text-white px-4 py-2 rounded-full group-hover:bg-blue-600 group-hover:text-white transition-colors uppercase tracking-widest shadow-inner">Attach</span>
                          </div>
                        </div>
                      ))}
                    </div>

                    <button 
                      onClick={handleUploadSubmit} disabled={uploading}
                      className="w-full bg-blue-600 hover:bg-blue-500 text-white font-black uppercase tracking-widest rounded-2xl px-8 py-5 shadow-[0_0_30px_rgba(37,99,235,0.4)] disabled:opacity-70 flex items-center justify-center hover:scale-[1.02] active:scale-95 transition-transform text-lg"
                    >
                      {uploading ? <><span className="w-6 h-6 border-[3px] border-white/30 border-t-white rounded-full animate-spin mr-3"/> Hashing Data...</> : "Run Execution"}
                    </button>
                  </motion.div>
                ) : (
                  <div className="space-y-8">
                    <div className="bg-black/40 border border-white/5 rounded-[2rem] p-8 hover:border-white/10 transition-colors">
                      <h3 className="text-slate-400 font-black mb-4 flex items-center gap-2 uppercase tracking-widest text-xs"><Zap className="w-4 h-4 text-blue-500"/> Output Value</h3>
                      <p className="text-white font-black mb-4 text-2xl leading-none">{selectedScheme.benefits}</p>
                      <p className="text-slate-400 text-base leading-relaxed font-medium">{selectedScheme.description}</p>
                    </div>
                    
                    <div className="bg-black/40 border border-white/5 rounded-[2rem] p-8 hover:border-white/10 transition-colors">
                      <h3 className="text-slate-400 font-black mb-6 flex items-center gap-2 uppercase tracking-widest text-xs"><Layers className="w-4 h-4 text-fuchsia-500"/> Integration Path</h3>
                      <div className="space-y-4">
                          {selectedScheme.howToApply.map((step: string, i: number) => (
                              <div key={i} className="flex gap-4 items-center bg-white/5 p-4 rounded-2xl border border-white/5">
                                  <div className="w-8 h-8 rounded-full bg-white/10 border border-white/20 flex items-center justify-center text-white font-black shrink-0">{i+1}</div>
                                  <p className="text-slate-200 font-bold">{step}</p>
                              </div>
                          ))}
                      </div>
                    </div>

                    <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row gap-5">
                      <Link href={`/chat?scheme=${selectedScheme.id}`} className="flex-1 bg-white/5 hover:bg-white/10 border border-white/5 text-white font-black uppercase tracking-widest rounded-2xl px-6 py-5 transition-colors flex items-center justify-center gap-2">💬 AI Consult</Link>
                      <button onClick={() => setIsApplying(true)} className="flex-[2] bg-blue-600 hover:bg-blue-500 text-white font-black uppercase tracking-widest rounded-2xl px-6 py-5 shadow-[0_0_30px_rgba(37,99,235,0.4)] transition-all flex items-center justify-center gap-3 group hover:scale-[1.02] active:scale-95">Compile Data <ArrowRight className="w-5 h-5 group-hover:translate-x-2 transition-transform" /></button>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}
