"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { ArrowLeft, Mail, KeyRound, Loader2, Link2 } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      router.push("/dashboard"); 
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-[#030308] flex flex-col justify-center relative overflow-hidden font-sans text-white">
      <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[150px] pointer-events-none mix-blend-screen animate-pulse" />
      <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-fuchsia-600/10 rounded-full blur-[120px] pointer-events-none mix-blend-screen" />
      <div className="absolute inset-0 bg-mesh opacity-50 pointer-events-none" />

      <div className="container mx-auto px-4 z-10">
        <Link href="/" className="absolute top-8 left-8 text-slate-400 hover:text-white flex items-center gap-2 font-bold transition-colors bg-white/5 backdrop-blur-md px-4 py-2 rounded-full border border-white/10">
          <ArrowLeft className="w-4 h-4 text-blue-500" /> Back to Home
        </Link>

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5, type: "spring" }}
          className="max-w-md mx-auto"
        >
          <div className="bg-[#05050A]/80 backdrop-blur-3xl border border-white/10 p-10 rounded-[2rem] shadow-[0_0_50px_rgba(0,0,0,0.8)] relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-transparent pointer-events-none" />
            
            <div className="text-center mb-10 relative z-10">
              <div className="w-16 h-16 bg-blue-500/10 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-blue-500/20 shadow-[0_0_20px_rgba(59,130,246,0.3)]"><Link2 className="w-8 h-8 text-blue-400" /></div>
              <h2 className="text-3xl font-black text-white mb-2 tracking-tight">Access Portal</h2>
              <p className="text-slate-400 font-medium">Verify credentials to access your registry.</p>
            </div>

            <form onSubmit={handleLogin} className="space-y-6 relative z-10">
              <div className="space-y-2">
                <label className="text-xs font-black text-slate-400 uppercase tracking-widest pl-2">Email Identity</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none"><Mail className="w-5 h-5 text-slate-500" /></div>
                  <input type="email" required onChange={(e) => setFormData({...formData, email: e.target.value})} className="w-full bg-black/50 border border-white/10 rounded-2xl pl-14 pr-4 py-4 text-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-inner font-medium placeholder:text-slate-600" placeholder="name@example.com" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-black text-slate-400 uppercase tracking-widest pl-2">Passcode</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none"><KeyRound className="w-5 h-5 text-slate-500" /></div>
                  <input type="password" required onChange={(e) => setFormData({...formData, password: e.target.value})} className="w-full bg-black/50 border border-white/10 rounded-2xl pl-14 pr-4 py-4 text-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-inner font-medium placeholder:text-slate-600" placeholder="••••••••" />
                </div>
              </div>

              <button type="submit" disabled={isLoading} className="w-full mt-8 bg-blue-600 hover:bg-blue-500 text-white font-black uppercase tracking-widest rounded-2xl px-4 py-5 transition-all shadow-[0_0_30px_rgba(37,99,235,0.4)] disabled:opacity-70 flex items-center justify-center gap-3 hover:scale-[1.02] active:scale-[0.98]">
                {isLoading ? <><Loader2 className="w-5 h-5 animate-spin" /> Authenticating...</> : "Initialize Session"}
              </button>
            </form>

            <p className="text-center text-slate-400 mt-10 text-sm font-medium relative z-10">
              Not connected to the registry? <Link href="/register" className="text-blue-400 hover:text-blue-300 font-black transition-colors ml-1">Create node</Link>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
