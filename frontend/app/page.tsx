"use client";

import { useState, useEffect } from "react";
import { FiUploadCloud, FiClock, FiCheckCircle, FiAlertCircle, FiAward, FiPlus, FiFileText, FiSearch, FiExternalLink } from "react-icons/fi";

export default function HireLightDashboard() {
  const [jobDescription, setJobDescription] = useState("");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [history, setHistory] = useState<string[]>([]);

  useEffect(() => {
    const savedHistory = localStorage.getItem("hire-light-history");
    if (savedHistory) setHistory(JSON.parse(savedHistory));
  }, []);

  // NEW: Function to load previous audits from the history box
  const fetchAudit = async (batchId: string) => {
    setIsAnalyzing(true);
    setAnalysisData(null);
    try {
      const res = await fetch(`http://localhost:8000/status/${batchId}`);
      const data = await res.json();
      setAnalysisData(data);
      setIsAnalyzing(false);
    } catch (err) {
      setIsAnalyzing(false);
      alert("Could not retrieve this historical audit.");
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setSelectedFiles(Array.from(e.target.files));
  };

  const startAudit = async () => {
    if (!jobDescription || selectedFiles.length === 0) return alert("Fill all fields!");
    setIsAnalyzing(true);
    setAnalysisData(null);

    const formData = new FormData();
    formData.append("job_description", jobDescription);
    selectedFiles.forEach((file) => formData.append("files", file));

    try {
      const response = await fetch("http://localhost:8000/upload-batch", { method: "POST", body: formData });
      const { batch_id } = await response.json();
      
      const newHistory = [batch_id, ...history].slice(0, 10);
      setHistory(newHistory);
      localStorage.setItem("hire-light-history", JSON.stringify(newHistory));

      const poll = setInterval(async () => {
        const res = await fetch(`http://localhost:8000/status/${batch_id}`);
        const data = await res.json();
        setAnalysisData(data);
        if (data.status === "completed" || data.status === "failed") {
          clearInterval(poll);
          setIsAnalyzing(false);
        }
      }, 2000);
    } catch (err) {
      setIsAnalyzing(false);
      alert("Backend Connection Error");
    }
  };

  return (
    <div className="flex h-screen bg-[#F8FAFC] text-slate-800 font-sans">
      {/* SIDEBAR: Dark & High Contrast */}
      <aside className="w-80 bg-slate-900 p-8 flex flex-col shadow-2xl z-30">
        <div className="mb-12">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-indigo-500 rounded-xl flex items-center justify-center text-white font-black shadow-lg shadow-indigo-500/20 transition-transform hover:rotate-6">H</div>
            <h1 className="text-2xl font-black tracking-tight text-white">Hire-Light</h1>
          </div>
          <p className="text-[10px] font-bold text-indigo-400 uppercase tracking-[0.2em]">Forensic Decision Engine</p>
        </div>

        <div className="flex-1 overflow-y-auto">
          <h3 className="flex items-center gap-2 text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-6">
            <FiClock className="text-indigo-400" /> Recent Audits
          </h3>
          <div className="space-y-4">
            {history.map((id) => (
              <div 
                key={id} 
                onClick={() => fetchAudit(id)} // FIX: History now clickable
                className="group flex items-center justify-between p-4 rounded-2xl bg-slate-800/30 border border-slate-700/50 hover:border-indigo-500/50 hover:bg-slate-800 transition-all cursor-pointer active:scale-95"
              >
                <span className="text-[10px] font-mono text-slate-500 group-hover:text-slate-200 truncate pr-2">ID: {id.slice(0, 15)}...</span>
                <FiExternalLink className="text-slate-600 group-hover:text-indigo-400" size={14} />
              </div>
            ))}
          </div>
        </div>

        <button 
          onClick={() => { setAnalysisData(null); setSelectedFiles([]); setJobDescription(""); }}
          className="mt-8 flex items-center justify-center gap-3 py-4 w-full bg-indigo-600 text-white rounded-2xl text-sm font-bold hover:bg-indigo-500 transition-all shadow-xl shadow-indigo-600/20"
        >
          <FiPlus size={18} /> NEW AUDIT
        </button>
      </aside>

      {/* MAIN CONTENT: Rich Contrast & Depth */}
      <main className="flex-1 overflow-y-auto p-12 bg-[#F1F5F9] relative">
        <div className="max-w-6xl mx-auto">
          {!analysisData ? (
            <div className="animate-in fade-in slide-in-from-bottom-8 duration-1000">
              <div className="mb-16">
                <h2 className="text-6xl font-black text-slate-900 mb-6 tracking-tight leading-[1.1]">
                  Verify <span className="text-indigo-600 underline decoration-indigo-100 decoration-8 underline-offset-8">Excellence</span>.
                </h2>
                <p className="text-slate-500 text-xl max-w-2xl leading-relaxed">
                  Identify your <span className="text-slate-900 font-bold">Best-Fit Candidate</span> by auditing evidence across multiple resumes instantly.
                </p>
              </div>

              <div className="grid grid-cols-1 xl:grid-cols-5 gap-10">
                {/* Requirements Panel - Glass Effect */}
                <div className="xl:col-span-3 bg-white/60 backdrop-blur-md p-10 rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-white">
                  <h4 className="font-bold text-lg flex items-center gap-3 mb-8 text-slate-700"><FiSearch className="text-indigo-500" /> Ideal Profile</h4>
                  <textarea
                    className="w-full h-80 bg-slate-100/50 border-2 border-slate-200/50 rounded-3xl p-6 text-base focus:bg-white focus:border-indigo-500 focus:ring-0 transition-all resize-none placeholder:text-slate-400"
                    placeholder="Describe the role in detail..."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                  />
                </div>

                {/* Upload Panel - High Contrast Border */}
                <div className="xl:col-span-2 flex flex-col gap-8">
                   <div className="flex-1 bg-white/60 backdrop-blur-md p-10 rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-white flex flex-col">
                      <h4 className="font-bold text-lg flex items-center gap-3 mb-8 text-slate-700"><FiUploadCloud className="text-indigo-500" /> Resumes</h4>
                      <div className="flex-1 border-2 border-dashed border-slate-300 rounded-3xl flex flex-col items-center justify-center bg-slate-100/50 hover:bg-indigo-50 hover:border-indigo-300 transition-all relative group cursor-pointer">
                        <input type="file" multiple accept=".pdf" onChange={handleFileChange} className="absolute inset-0 opacity-0 cursor-pointer" />
                        <FiFileText className="text-5xl text-slate-300 mb-4 group-hover:text-indigo-500 group-hover:rotate-6 transition-all" />
                        <p className="text-sm font-bold text-slate-400 group-hover:text-indigo-600 px-6 text-center">
                          {selectedFiles.length > 0 ? `${selectedFiles.length} Selected` : "Drop PDFs Here"}
                        </p>
                      </div>
                   </div>
                   
                   <button 
                    onClick={startAudit}
                    disabled={isAnalyzing || selectedFiles.length === 0}
                    className="w-full py-6 bg-slate-900 text-white font-black text-lg rounded-[2rem] shadow-2xl shadow-slate-900/40 hover:bg-indigo-600 transition-all disabled:opacity-30 active:scale-95"
                  >
                    {isAnalyzing ? "AUDITING..." : "EXECUTE FORENSIC CHAIN"}
                  </button>
                </div>
              </div>
            </div>
          ) : (
            /* RESULTS STAGE - Card Contrast */
            <div className="animate-in slide-in-from-right-12 duration-700">
               <div className="flex items-end justify-between mb-12">
                  <h2 className="text-4xl font-black text-slate-900 tracking-tight">Audit Report</h2>
                  <div className="flex items-center gap-4 bg-white px-6 py-2 rounded-full shadow-sm border border-slate-200">
                    <span className="text-2xl font-black text-indigo-600">{analysisData.progress}%</span>
                    <div className="w-24 h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full bg-indigo-500" style={{ width: `${analysisData.progress}%` }}></div>
                    </div>
                  </div>
               </div>

               <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
                  {analysisData.results?.sort((a:any, b:any) => b.score - a.score).map((candidate: any, idx: number) => (
                    <div key={idx} className={`group relative p-1 bg-gradient-to-br from-white to-slate-50 rounded-[3rem] shadow-2xl transition-all ${idx === 0 ? 'ring-4 ring-indigo-500/10' : ''}`}>
                      <div className={`h-full w-full bg-white p-10 rounded-[2.8rem] border-2 ${idx === 0 ? 'border-indigo-500' : 'border-transparent'}`}>
                        {idx === 0 && (
                          <div className="absolute -top-6 left-10 bg-indigo-600 text-white px-6 py-2 rounded-full shadow-xl flex items-center gap-2 text-xs font-black uppercase tracking-widest">
                            <FiAward /> Top Pick
                          </div>
                        )}
                        
                        <div className="flex justify-between items-start mb-8">
                          <div>
                            <h3 className="text-2xl font-black text-slate-900">{candidate.filename}</h3>
                            <p className="text-[10px] font-black text-indigo-500 uppercase tracking-widest mt-1">{candidate.brand_alignment || "Technical Match"}</p>
                          </div>
                          <div className="text-right">
                            <div className="text-4xl font-black text-slate-900">{candidate.score}</div>
                            <div className="text-[10px] font-bold text-slate-800 uppercase tracking-widest">Score</div>
                          </div>
                        </div>

                        <div className="p-6 bg-slate-50 rounded-3xl mb-8 border-l-4 border-indigo-500 shadow-inner">
                          <p className="text-sm text-slate-600 leading-relaxed italic">"{candidate.summary}"</p>
                        </div>

                        <div className="grid grid-cols-2 gap-6 pt-8 border-t border-slate-100">
                          <div>
                            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                              <FiCheckCircle className="text-emerald-500" /> Verified
                            </p>
                            <div className="flex flex-wrap gap-2">
                              {(candidate.verified_skills || []).slice(0, 4).map((s: any, i: number) => (
                                <span key={i} className="text-[9px] font-black bg-emerald-50 text-emerald-700 px-3 py-1.5 rounded-lg border border-emerald-100 uppercase">{s.skill || s}</span>
                              ))}
                            </div>
                          </div>
                          <div>
                            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                              <FiAlertCircle className="text-amber-500" /> Next Steps
                            </p>
                            <ul className="space-y-2">
                              {(candidate.improvement_tips || []).slice(0, 2).map((tip: string, i: number) => (
                                <li key={i} className="text-[11px] text-slate-500 leading-snug">• {tip}</li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
               </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}