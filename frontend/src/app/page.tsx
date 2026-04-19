"use client";

import React, { useEffect, useState } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowRight, Shield, Search, MessageSquare, Activity, Globe, Database } from "lucide-react";
import Link from 'next/link';

export default function LandingPage() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -150]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  const [liveUsers, setLiveUsers] = useState(14205);
  useEffect(() => {
    const interval = setInterval(() => setLiveUsers(prev => prev + Math.floor(Math.random() * 5)), 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative min-h-screen bg-slate-50 text-slate-900 overflow-hidden font-sans selection:bg-blue-500/20">
      
      {/* Enterprise Light-Mode Background Architecture */}
      <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] opacity-40"></div>
        <motion.div 
          animate={{ x: [0, 50, 0], y: [0, -30, 0] }} transition={{ duration: 15, repeat: Infinity, ease: "easeInOut" }}
          className="absolute -top-[10%] -left-[5%] w-[50%] h-[50%] rounded-full bg-blue-400/20 blur-[120px] mix-blend-multiply" 
        />
        <motion.div 
          animate={{ x: [0, -50, 0], y: [0, 60, 0] }} transition={{ duration: 20, repeat: Infinity, ease: "easeInOut", delay: 2 }}
          className="absolute top-[30%] -right-[10%] w-[60%] h-[60%] rounded-full bg-indigo-400/20 blur-[150px] mix-blend-multiply" 
        />
        <motion.div 
          animate={{ scale: [1, 1.1, 1], opacity: [0.3, 0.5, 0.3] }} transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          className="absolute -bottom-[20%] left-[20%] w-[60%] h-[50%] rounded-full bg-emerald-300/20 blur-[150px] mix-blend-multiply" 
        />
      </div>

      <div className="relative z-10 flex flex-col h-full">
        <nav className="container mx-auto px-6 py-6 flex justify-between items-center border-b border-slate-200/50 backdrop-blur-xl bg-white/30 sticky top-0 z-50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-black tracking-tight text-slate-900">GovScheme <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">AI</span></span>
          </div>
          <div className="hidden md:flex gap-8 text-sm font-bold text-slate-600">
            <a href="#features" className="hover:text-blue-600 transition-colors">Platform Engine</a>
            <a href="#features" className="hover:text-blue-600 transition-colors">AI Architecture</a>
            <a href="#features" className="hover:text-blue-600 transition-colors flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" /> 
              Live Stats
            </a>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login" className="text-sm font-bold text-slate-600 hover:text-blue-600 transition-colors hidden sm:block">
              Client Login
            </Link>
            <Link href="/form" className="text-sm font-bold bg-slate-900 text-white px-6 py-2.5 rounded-full hover:bg-blue-600 hover:scale-105 transition-all shadow-xl shadow-slate-900/10">
              Initialize Portal
            </Link>
          </div>
        </nav>

        <main className="container mx-auto px-6 pt-24 pb-32 flex flex-col items-center">
          <motion.div style={{ opacity, y }} className="max-w-5xl mx-auto text-center flex flex-col items-center">
            <motion.div 
              initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-3 px-5 py-2.5 rounded-full bg-white/80 border border-blue-100 text-blue-700 text-xs font-black uppercase tracking-widest mb-10 shadow-sm backdrop-blur-md"
            >
              <div className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-500 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-600"></span>
              </div>
              System Core Online • {liveUsers.toLocaleString()} Verifications Today
            </motion.div>
            
            <motion.h1 
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.1 }}
              className="text-6xl md:text-8xl font-black tracking-tighter mb-8 leading-[1.1] text-slate-900"
            >
              Unlock Government <br />
              Benefits in <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">Real-Time.</span>
            </motion.h1>
            
            <motion.p 
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1, delay: 0.3 }}
              className="text-xl text-slate-600 mb-12 max-w-2xl mx-auto leading-relaxed font-medium"
            >
              Connect your demographic profile to our Multi-Agent RAG pipeline. We process 14,000+ schemes across registries to instantly match, verify, and automatically apply for you.
            </motion.p>

            <motion.div 
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.5 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-5 w-full sm:w-auto"
            >
              <Link href="/register" className="w-full sm:w-auto px-8 py-4 bg-blue-600 text-white rounded-full font-bold shadow-xl shadow-blue-600/30 flex items-center justify-center gap-2 hover:bg-blue-700 hover:shadow-blue-600/40 hover:-translate-y-0.5 transition-all text-sm tracking-wide">
                Launch Matching Hub <ArrowRight className="w-5 h-5" />
              </Link>
              <Link href="/chat" className="w-full sm:w-auto px-8 py-4 bg-white/90 backdrop-blur-xl border border-slate-200 text-slate-800 rounded-full font-bold shadow-lg shadow-slate-200/40 flex items-center justify-center gap-2 hover:bg-white hover:-translate-y-0.5 transition-all text-sm tracking-wide group">
                <MessageSquare className="w-5 h-5 text-indigo-500 group-hover:scale-110 transition-transform" /> Query AI Database
              </Link>
            </motion.div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 60 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1, delay: 0.7 }}
            className="w-full max-w-5xl mt-24 relative p-4 sm:p-6 rounded-[2.5rem] bg-white/40 backdrop-blur-3xl border border-white/60 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)]"
          >
            <div className="absolute inset-0 bg-gradient-to-b from-white/60 to-white/10 rounded-[2.5rem] pointer-events-none" />
            
            <div className="bg-white rounded-[2rem] overflow-hidden flex flex-col shadow-sm border border-slate-100 relative z-10 w-full">
              <div className="h-14 bg-slate-50 border-b border-slate-100 flex items-center px-6 justify-between">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-rose-400 shadow-inner" />
                  <div className="w-3 h-3 rounded-full bg-amber-400 shadow-inner" />
                  <div className="w-3 h-3 rounded-full bg-emerald-400 shadow-inner" />
                </div>
                <div className="px-3 py-1 bg-blue-50 text-blue-600 rounded-lg text-xs font-mono flex items-center gap-2 font-semibold">
                  <Database className="w-3.5 h-3.5" /> SECURE AI CONNECTION
                </div>
              </div>
              <div className="p-8 sm:p-10 grid md:grid-cols-3 gap-8 bg-gradient-to-b from-white to-slate-50/50">
                {[
                  { title: "Network Status", value: "Optimal", text: "Vector Database synced 2 mins ago.", icon: <Globe className="text-blue-500"/>, metric: "12ms", bg: "bg-blue-50", border: "border-blue-100" },
                  { title: "RAG Accuracy", value: "99.8%", text: "Precision matched across schemas.", icon: <Search className="text-indigo-500"/>, metric: "+1.2%", bg: "bg-indigo-50", border: "border-indigo-100" },
                  { title: "Active Agents", value: "3 Nodes", text: "Eligibility, Explainer, and Guide bots.", icon: <Activity className="text-emerald-500"/>, metric: "Live", bg: "bg-emerald-50", border: "border-emerald-100" }
                ].map((item, i) => (
                  <div key={i} className="bg-white p-6 rounded-2xl border border-slate-100 relative overflow-hidden group hover:shadow-xl hover:shadow-slate-200/40 transition-all hover:-translate-y-1">
                    <div className="flex justify-between items-start mb-6">
                      <div className={`p-3 rounded-xl ${item.bg} ${item.border} border`}>
                        {item.icon}
                      </div>
                      <span className="text-xs font-mono font-semibold text-slate-600 bg-slate-50 border border-slate-100 px-2.5 py-1 rounded-md">{item.metric}</span>
                    </div>
                    <h3 className="text-slate-500 font-bold text-xs mb-1.5 uppercase tracking-widest">{item.title}</h3>
                    <p className="text-slate-900 text-3xl font-black tracking-tight mb-2">{item.value}</p>
                    <p className="text-slate-500 text-sm font-medium leading-relaxed">{item.text}</p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </main>
      </div>
    </div>
  );
}
