"use client";

import React, { useState, useRef, useEffect } from "react";
import { Send, User, ChevronLeft, Bot } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I am your AI Scheme Guide. I've analyzed your profile. How can I help you with your applications today?" }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await fetch("http://localhost:8000/chat/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage, session_id: "default-session" }) 
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, { role: "assistant", content: data.response }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { 
        role: "assistant", 
        content: "I couldn't contact the Intelligence Core right now. Ensure your FastAPI server is online." 
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#030308] text-white">
      <header className="border-b border-white/5 bg-[#05050A]/80 backdrop-blur p-4 flex items-center justify-between shadow-2xl z-10">
        <div className="flex items-center gap-4">
          <Link href="/dashboard" className="p-2 bg-white/5 hover:bg-blue-600/20 rounded-xl text-slate-400 hover:text-blue-400 transition-colors border border-transparent hover:border-blue-500/30">
            <ChevronLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="font-black text-white text-lg flex items-center gap-2">
              <Bot className="w-5 h-5 text-blue-500" />
              Eligibility & Application Guide
            </h1>
            <p className="text-xs text-slate-400 font-medium tracking-wide">Powered by Multi-Agent Network</p>
          </div>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 relative no-scrollbar">
        <div className="absolute inset-0 bg-mesh opacity-30 z-0 pointer-events-none" />
        
        {messages.map((msg, i) => (
          <motion.div 
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} key={i} 
            className={`flex relative z-10 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div className={`flex items-start gap-3 max-w-[85%] md:max-w-[70%] ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm ${msg.role === "user" ? "bg-blue-600 text-white" : "bg-black text-blue-400 border border-white/10"}`}>
                {msg.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>
              <div className={`p-4 rounded-2xl shadow-xl ${msg.role === "user" ? "bg-blue-600 text-white rounded-tr-sm" : "bg-white/5 border border-white/10 text-slate-200 rounded-tl-sm backdrop-blur-md"}`}>
                <p className="leading-relaxed whitespace-pre-wrap font-medium text-sm md:text-base">{msg.content}</p>
              </div>
            </div>
          </motion.div>
        ))}
        {isTyping && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start relative z-10">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-black text-blue-400 border border-white/10 flex items-center justify-center">
                <Bot className="w-4 h-4" />
              </div>
              <div className="p-4 rounded-2xl bg-white/5 border border-white/10 rounded-tl-sm flex gap-1 backdrop-blur-md">
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></span>
                <span className="w-2 h-2 bg-fuchsia-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
              </div>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </main>

      <footer className="p-4 bg-[#05050A]/90 border-t border-white/5 backdrop-blur z-10">
        <form onSubmit={handleSend} className="max-w-4xl mx-auto flex gap-3">
          <input 
            type="text" value={input} onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about required documents, eligibility, or application steps..."
            className="flex-1 bg-black/50 border border-white/10 text-white rounded-2xl px-5 py-4 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-inner placeholder:text-slate-500 font-medium"
          />
          <button 
            type="submit" disabled={!input.trim() || isTyping}
            className="bg-blue-600 hover:bg-blue-500 shadow-[0_0_20px_rgba(37,99,235,0.4)] text-white p-4 rounded-2xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex flex-shrink-0 items-center justify-center hover:scale-105 active:scale-95 border border-blue-400/50"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </footer>
    </div>
  );
}
