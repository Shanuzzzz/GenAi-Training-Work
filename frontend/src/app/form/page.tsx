"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft, ArrowRight, Database, Globe, Activity, Cpu, Zap } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function DemographicForm() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const [formData, setFormData] = useState({
    age: "", gender: "", state: "", caste: "", income: "", occupation: ""
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if(step < 3) {
      setStep(step + 1);
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      router.push("/dashboard");
    }, 2500);
  };

  return (
    <div className="min-h-screen bg-[#030308] flex flex-col justify-center relative overflow-hidden font-sans text-white">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-600/10 rounded-full blur-[200px] pointer-events-none mix-blend-screen animate-pulse" />
      <div className="absolute inset-0 bg-mesh opacity-50 pointer-events-none" />

      <div className="container mx-auto px-4 z-10 py-12 relative">
        <Link href="/" className="absolute top-4 md:top-8 left-4 md:left-8 text-slate-400 hover:text-white flex items-center gap-2 transition-colors font-bold bg-white/5 backdrop-blur-md px-4 py-2 rounded-full shadow-lg border border-white/10">
          <ArrowLeft className="w-5 h-5 text-blue-500" /> Main Interface
        </Link>

        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="max-w-2xl mx-auto mt-16 md:mt-0">
          <div className="mb-12">
            <div className="flex justify-between items-end mb-4">
              <div>
                <h2 className="text-3xl md:text-4xl font-black text-white mb-2 tracking-tight drop-shadow-lg">Configure Profile</h2>
                <p className="text-slate-400 font-medium">Initialize context for the Multi-Agent engine.</p>
              </div>
              <span className="text-blue-400 font-mono font-bold bg-blue-500/10 px-4 py-1.5 rounded-full border border-blue-500/20 shadow-[0_0_15px_rgba(59,130,246,0.3)]">Step {step}/3</span>
            </div>
            <div className="w-full bg-black/60 rounded-full h-2 overflow-hidden shadow-inner border border-white/5">
              <motion.div 
                initial={false} animate={{ width: `${(step / 3) * 100}%` }} transition={{ duration: 0.5, ease: "easeInOut" }}
                className="bg-gradient-to-r from-blue-600 to-fuchsia-500 h-full shadow-[0_0_15px_rgba(59,130,246,0.8)] rounded-full" 
              />
            </div>
          </div>

          <div className="bg-[#05050A]/80 backdrop-blur-3xl border border-white/10 rounded-[2rem] p-8 md:p-12 shadow-[0_0_50px_rgba(0,0,0,0.8)] relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50" />
            
            <form onSubmit={handleSubmit} className="relative z-10 min-h-[300px] flex flex-col justify-between">
              <AnimatePresence mode="wait">
                {step === 1 && (
                  <motion.div key="step1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-8">
                    <h3 className="text-2xl font-black text-white mb-6 flex items-center gap-3"><Database className="w-6 h-6 text-blue-500" /> Core Demographics</h3>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div className="space-y-3">
                        <label className="text-xs font-black text-slate-400 uppercase tracking-widest pl-2">Age</label>
                        <input type="number" required value={formData.age} onChange={(e) => setFormData({...formData, age: e.target.value})} className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-inner text-lg placeholder:text-slate-600 font-medium" placeholder="Ex: 28" />
                      </div>
                      <div className="space-y-3">
                        <label className="text-xs font-black text-slate-400 uppercase tracking-widest pl-2">Gender</label>
                        <select required value={formData.gender} onChange={(e) => setFormData({...formData, gender: e.target.value})} className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-all appearance-none shadow-inner text-lg font-medium cursor-pointer [&>option]:bg-slate-900">
                          <option value="">Select identity...</option>
                          <option value="Male">Male</option>
                          <option value="Female">Female</option>
                          <option value="Other">Other</option>
                        </select>
                      </div>
                    </div>
                  </motion.div>
                )}

                {step === 2 && (
                  <motion.div key="step2" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-8">
                     <h3 className="text-2xl font-black text-white mb-6 flex items-center gap-3"><Globe className="w-6 h-6 text-fuchsia-500" /> Regional Vectors</h3>
                    <div className="space-y-3">
                      <label className="text-xs font-black text-slate-400 uppercase tracking-widest pl-2">Geographic State</label>
                      <input type="text" required value={formData.state} onChange={(e) => setFormData({...formData, state: e.target.value})} className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-inner text-lg placeholder:text-slate-600 font-medium" placeholder="Ex: Maharashtra" />
                    </div>
                    <div className="space-y-3 pt-2">
                      <label className="text-xs font-black text-slate-400 uppercase tracking-widest pl-2">Social Category</label>
                      <select required value={formData.caste} onChange={(e) => setFormData({...formData, caste: e.target.value})} className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-all appearance-none shadow-inner text-lg font-medium cursor-pointer [&>option]:bg-slate-900">
                        <option value="">Select registry classification...</option>
                        <option value="General">General</option>
                        <option value="OBC">OBC</option>
                        <option value="SC">SC</option>
                        <option value="ST">ST</option>
                      </select>
                    </div>
                  </motion.div>
                )}

                {step === 3 && (
                  <motion.div key="step3" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-8">
                    <h3 className="text-2xl font-black text-white mb-6 flex items-center gap-3"><Activity className="w-6 h-6 text-cyan-400" /> Financial Parameters</h3>
                    <div className="space-y-3">
                      <label className="text-xs font-black text-slate-400 uppercase tracking-widest pl-2">Annual Income (₹)</label>
                      <input type="number" required value={formData.income} onChange={(e) => setFormData({...formData, income: e.target.value})} className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-inner text-lg placeholder:text-slate-600 font-medium" placeholder="Ex: 250000" />
                    </div>
                    <div className="space-y-3 pt-2">
                      <label className="text-xs font-black text-slate-400 uppercase tracking-widest pl-2">Primary Occupation</label>
                      <input type="text" required value={formData.occupation} onChange={(e) => setFormData({...formData, occupation: e.target.value})} className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-inner text-lg placeholder:text-slate-600 font-medium" placeholder="Ex: Farmer, Student, SME Business" />
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              <div className="mt-12 flex justify-between gap-4">
                {step > 1 ? (
                  <button type="button" onClick={() => setStep(step - 1)} className="px-8 py-5 rounded-2xl font-black text-white uppercase tracking-widest bg-white/5 border border-white/10 hover:bg-white/10 transition-colors flex items-center gap-2 shadow-lg">
                    <ArrowLeft className="w-5 h-5 text-fuchsia-500" /> Back
                  </button>
                ) : <div />}

                <button 
                  type="submit" 
                  disabled={loading}
                  className="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-black uppercase tracking-widest rounded-2xl px-8 py-5 transition-all shadow-[0_0_30px_rgba(37,99,235,0.4)] hover:scale-[1.02] active:scale-[0.98] disabled:opacity-75 flex items-center justify-center gap-3 ml-auto text-sm md:text-base border border-blue-400/50"
                >
                  {loading ? (
                    <span className="flex items-center gap-3">
                      <Cpu className="w-5 h-5 animate-pulse text-white" /> Processing Profile...
                    </span>
                  ) : step === 3 ? (
                    <span className="flex items-center gap-2">Execute Analysis <Zap className="w-5 h-5" /></span>
                  ) : (
                    <span className="flex items-center gap-2">Next Sequence <ArrowRight className="w-5 h-5" /></span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
