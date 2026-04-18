import { useState, useRef } from "react";

const STEPS = ["home", "upload", "analysis", "interview", "simulation"];

const callClaude = async (systemPrompt, userMessage) => {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1000,
      system: systemPrompt,
      messages: [{ role: "user", content: userMessage }],
    }),
  });
  const data = await response.json();
  return data.content[0].text;
};

export default function JobWinApp() {
  const [step, setStep] = useState("home");
  const [cvText, setCvText] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [simMessages, setSimMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentQ, setCurrentQ] = useState(0);
  const fileRef = useRef();

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => setCvText(ev.target.result);
    reader.readAsText(file);
  };

  const analyzeCV = async () => {
    if (!cvText && !jobTitle) return;
    setLoading(true);
    setStep("analysis");
    try {
      const result = await callClaude(
        `أنت خبير في التوظيف والموارد البشرية في المغرب. تحلل CVs وتعطي نصائح عملية بالدارجة المغربية. ردودك تكون واضحة ومنظمة.`,
        `حلل ليا هاد CV ديالي باش نقدر نلقى خدمة ك${jobTitle || "أي منصب"} فالمغرب:

${cvText || "ما عندي CV مكتوب بعد، عطيني نصائح عامة"}

عطيني:
1. **نقاط القوة** (3 نقاط)
2. **نقاط الضعف** (3 نقاط)  
3. **شنو نزيد أو نبدل** (3 نصائح عملية)
4. **تقييم عام** من 10

الجواب بالدارجة المغربية وكون محدد وعملي.`
      );
      setAnalysis(result);
    } catch (e) {
      setAnalysis("وقع مشكل تقني، عاود المحاولة.");
    }
    setLoading(false);
  };

  const prepareInterview = async () => {
    setLoading(true);
    setStep("interview");
    try {
      const result = await callClaude(
        `أنت coach تحضير مقابلات عمل في المغرب. تعطي أسئلة حقيقية مع أجوبة جاهزة بالدارجة.`,
        `حضر ليا 5 أسئلة مقابلة عمل ل${jobTitle || "منصب عام"} مع جواب مثالي لكل سؤال.

الفورمات يكون هكذا بالضبط (JSON فقط بدون أي كلام زيادة):
[
  {"سؤال": "...", "جواب": "..."},
  {"سؤال": "...", "جواب": "..."},
  {"سؤال": "...", "جواب": "..."},
  {"سؤال": "...", "جواب": "..."},
  {"سؤال": "...", "جواب": "..."}
]`
      );
      try {
        const clean = result.replace(/```json|```/g, "").trim();
        setQuestions(JSON.parse(clean));
      } catch {
        setQuestions([
          { سؤال: "علاش بغيتي تخدم معنا؟", جواب: "لأني كاين عندي الشغف والخبرة اللي محتاجينها..." },
          { سؤال: "شنو هي نقاط قوتك؟", جواب: "أنا شخص منظم وعندي مهارات تواصل قوية..." },
        ]);
      }
    } catch (e) {
      setQuestions([]);
    }
    setLoading(false);
  };

  const startSimulation = () => {
    setStep("simulation");
    setSimMessages([
      { role: "interviewer", text: `مرحبا! أنا غنجري معك simulation ديال مقابلة عمل ل${jobTitle || "المنصب"}. جاوب بشكل طبيعي بالدارجة. نبداو؟ 👋\n\nالسؤال الأول: علاش بغيتي تخدم معنا؟` }
    ]);
  };

  const sendSimMessage = async () => {
    if (!userInput.trim()) return;
    const newMessages = [...simMessages, { role: "user", text: userInput }];
    setSimMessages(newMessages);
    setUserInput("");
    setLoading(true);
    try {
      const history = newMessages.map(m => `${m.role === "interviewer" ? "Interviewer" : "Candidate"}: ${m.text}`).join("\n");
      const reply = await callClaude(
        `أنت مسؤول توظيف مغربي تجري مقابلة عمل. تتكلم بالدارجة. بعد كل جواب تعطي feedback قصير (جيد/ضعيف وليش) ثم تسأل سؤال جديد. بعد 4 أسئلة تعطي تقييم نهائي.`,
        `سياق المقابلة:\n${history}\n\nاستمر في المقابلة - أعطي feedback على الجواب الأخير وسأل سؤال جديد.`
      );
      setSimMessages([...newMessages, { role: "interviewer", text: reply }]);
    } catch (e) {
      setSimMessages([...newMessages, { role: "interviewer", text: "وقع مشكل، عاود." }]);
    }
    setLoading(false);
  };

  const styles = {
    app: {
      minHeight: "100vh",
      background: "linear-gradient(135deg, #0a0a0a 0%, #0d1f0d 50%, #0a1a0a 100%)",
      color: "#e8f5e8",
      fontFamily: "'Cairo', 'Segoe UI', sans-serif",
      direction: "rtl",
      padding: "0",
    },
    header: {
      background: "rgba(0,0,0,0.6)",
      backdropFilter: "blur(10px)",
      borderBottom: "1px solid #1a4d1a",
      padding: "16px 24px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      position: "sticky",
      top: 0,
      zIndex: 100,
    },
    logo: {
      fontSize: "22px",
      fontWeight: "800",
      color: "#4ade80",
      letterSpacing: "-0.5px",
    },
    badge: {
      background: "#1a3d1a",
      border: "1px solid #2d6b2d",
      color: "#4ade80",
      padding: "4px 12px",
      borderRadius: "20px",
      fontSize: "12px",
    },
    hero: {
      textAlign: "center",
      padding: "80px 24px 60px",
      maxWidth: "600px",
      margin: "0 auto",
    },
    heroTitle: {
      fontSize: "clamp(32px, 8vw, 52px)",
      fontWeight: "900",
      lineHeight: "1.1",
      marginBottom: "16px",
      background: "linear-gradient(135deg, #4ade80, #86efac, #ffffff)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
    },
    heroSub: {
      fontSize: "16px",
      color: "#86efac",
      marginBottom: "12px",
      opacity: 0.8,
    },
    heroDesc: {
      fontSize: "14px",
      color: "#a0a0a0",
      marginBottom: "40px",
      lineHeight: "1.8",
    },
    steps: {
      display: "flex",
      justifyContent: "center",
      gap: "8px",
      flexWrap: "wrap",
      marginBottom: "40px",
    },
    stepBadge: {
      background: "#0d1f0d",
      border: "1px solid #2d6b2d",
      color: "#4ade80",
      padding: "8px 16px",
      borderRadius: "30px",
      fontSize: "13px",
      display: "flex",
      alignItems: "center",
      gap: "6px",
    },
    btn: {
      background: "linear-gradient(135deg, #16a34a, #15803d)",
      color: "#fff",
      border: "none",
      padding: "16px 40px",
      borderRadius: "50px",
      fontSize: "16px",
      fontWeight: "700",
      cursor: "pointer",
      fontFamily: "'Cairo', sans-serif",
      boxShadow: "0 0 30px rgba(74,222,128,0.3)",
      transition: "all 0.2s",
    },
    btnSecondary: {
      background: "transparent",
      color: "#4ade80",
      border: "1px solid #2d6b2d",
      padding: "12px 28px",
      borderRadius: "50px",
      fontSize: "14px",
      fontWeight: "600",
      cursor: "pointer",
      fontFamily: "'Cairo', sans-serif",
    },
    card: {
      background: "rgba(13,31,13,0.8)",
      border: "1px solid #1a4d1a",
      borderRadius: "20px",
      padding: "28px",
      margin: "0 auto 20px",
      maxWidth: "600px",
    },
    input: {
      width: "100%",
      background: "#0a140a",
      border: "1px solid #2d6b2d",
      color: "#e8f5e8",
      padding: "14px 16px",
      borderRadius: "12px",
      fontSize: "15px",
      fontFamily: "'Cairo', sans-serif",
      marginBottom: "16px",
      outline: "none",
      boxSizing: "border-box",
      direction: "rtl",
    },
    textarea: {
      width: "100%",
      background: "#0a140a",
      border: "1px solid #2d6b2d",
      color: "#e8f5e8",
      padding: "14px 16px",
      borderRadius: "12px",
      fontSize: "14px",
      fontFamily: "'Cairo', sans-serif",
      marginBottom: "16px",
      outline: "none",
      boxSizing: "border-box",
      direction: "rtl",
      minHeight: "140px",
      resize: "vertical",
    },
    label: {
      fontSize: "14px",
      color: "#86efac",
      marginBottom: "8px",
      display: "block",
      fontWeight: "600",
    },
    analysisText: {
      fontSize: "14px",
      lineHeight: "2",
      color: "#d1fae5",
      whiteSpace: "pre-wrap",
    },
    qCard: {
      background: "#0a140a",
      border: "1px solid #1a4d1a",
      borderRadius: "14px",
      padding: "20px",
      marginBottom: "16px",
    },
    qTitle: {
      color: "#4ade80",
      fontWeight: "700",
      fontSize: "15px",
      marginBottom: "10px",
    },
    qAnswer: {
      color: "#a0c0a0",
      fontSize: "13px",
      lineHeight: "1.8",
      borderTop: "1px solid #1a4d1a",
      paddingTop: "10px",
      marginTop: "8px",
    },
    chatBox: {
      maxHeight: "50vh",
      overflowY: "auto",
      marginBottom: "16px",
      display: "flex",
      flexDirection: "column",
      gap: "12px",
    },
    bubble: (role) => ({
      background: role === "interviewer" ? "#0d1f0d" : "#16a34a",
      border: role === "interviewer" ? "1px solid #2d6b2d" : "none",
      color: "#e8f5e8",
      padding: "14px 18px",
      borderRadius: role === "interviewer" ? "18px 18px 18px 4px" : "18px 18px 4px 18px",
      maxWidth: "85%",
      alignSelf: role === "interviewer" ? "flex-start" : "flex-end",
      fontSize: "14px",
      lineHeight: "1.7",
      whiteSpace: "pre-wrap",
    }),
    inputRow: {
      display: "flex",
      gap: "10px",
    },
    sectionTitle: {
      fontSize: "20px",
      fontWeight: "800",
      color: "#4ade80",
      marginBottom: "20px",
      textAlign: "center",
    },
    loader: {
      textAlign: "center",
      padding: "40px",
      color: "#4ade80",
      fontSize: "16px",
    },
    dots: {
      display: "inline-block",
      animation: "pulse 1s infinite",
    },
    backBtn: {
      background: "transparent",
      border: "none",
      color: "#4ade80",
      cursor: "pointer",
      fontSize: "14px",
      fontFamily: "'Cairo', sans-serif",
      padding: "8px 0",
      marginBottom: "16px",
      display: "flex",
      alignItems: "center",
      gap: "6px",
    },
    page: {
      padding: "24px 16px",
      maxWidth: "640px",
      margin: "0 auto",
    },
  };

  return (
    <div style={styles.app}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @keyframes fadeIn { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
        * { animation: none }
        .fade { animation: fadeIn 0.4s ease forwards }
        button:hover { opacity: 0.85 !important; transform: scale(0.98) }
      `}</style>

      {/* Header */}
      <div style={styles.header}>
        <div style={styles.logo}>💼 JobWin.ma</div>
        <div style={styles.badge}>🤖 مدعوم بالذكاء الاصطناعي</div>
      </div>

      {/* HOME */}
      {step === "home" && (
        <div style={styles.hero} className="fade">
          <div style={{ fontSize: "60px", marginBottom: "20px" }}>🎯</div>
          <div style={styles.heroTitle}>من CV حتى تاخذ الخدمة</div>
          <div style={styles.heroSub}>JobWin.ma — مرافقك الذكي للتوظيف فالمغرب</div>
          <div style={styles.heroDesc}>
            ماشي غير تحليل CV... بل نظام كامل كيرافقك حتى تنجح فالمقابلة 🇲🇦
          </div>
          <div style={styles.steps}>
            {["📄 تحليل CV", "💡 تحسينات", "❓ أسئلة جاهزة", "🎭 Simulation"].map(s => (
              <div key={s} style={styles.stepBadge}>{s}</div>
            ))}
          </div>
          <button style={styles.btn} onClick={() => setStep("upload")}>
            ابدا دابا — مجاناً 🚀
          </button>
        </div>
      )}

      {/* UPLOAD */}
      {step === "upload" && (
        <div style={styles.page} className="fade">
          <button style={styles.backBtn} onClick={() => setStep("home")}>← رجوع</button>
          <div style={styles.sectionTitle}>📄 تحليل CV ديالك</div>

          <div style={styles.card}>
            <label style={styles.label}>شنو المنصب اللي بغيتي؟</label>
            <input
              style={styles.input}
              placeholder="مثال: مهندس برمجيات، محاسب، مسير مبيعات..."
              value={jobTitle}
              onChange={e => setJobTitle(e.target.value)}
            />

            <label style={styles.label}>حط محتوى CV ديالك (كوبي-بيست)</label>
            <textarea
              style={styles.textarea}
              placeholder="حط هنا محتوى CV ديالك... أو وصف خبرتك ومهاراتك"
              value={cvText}
              onChange={e => setCvText(e.target.value)}
            />

            <div style={{ textAlign: "center" }}>
              <button style={styles.btn} onClick={analyzeCV}>
                🔍 حلل CV ديالي
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ANALYSIS */}
      {step === "analysis" && (
        <div style={styles.page} className="fade">
          <button style={styles.backBtn} onClick={() => setStep("upload")}>← رجوع</button>
          <div style={styles.sectionTitle}>💡 تحليل CV ديالك</div>

          {loading ? (
            <div style={styles.loader}>
              <div style={{ fontSize: "40px", marginBottom: "16px" }}>🤖</div>
              <div>كنحلل CV ديالك<span style={styles.dots}>...</span></div>
            </div>
          ) : (
            <>
              <div style={styles.card}>
                <div style={styles.analysisText}>{analysis}</div>
              </div>
              <div style={{ textAlign: "center", marginTop: "24px" }}>
                <button style={styles.btn} onClick={prepareInterview}>
                  ❓ حضر ليا أسئلة المقابلة
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* INTERVIEW PREP */}
      {step === "interview" && (
        <div style={styles.page} className="fade">
          <button style={styles.backBtn} onClick={() => setStep("analysis")}>← رجوع</button>
          <div style={styles.sectionTitle}>❓ أسئلة المقابلة + أجوبة جاهزة</div>

          {loading ? (
            <div style={styles.loader}>
              <div style={{ fontSize: "40px", marginBottom: "16px" }}>💭</div>
              <div>كنحضر الأسئلة ديالك<span style={styles.dots}>...</span></div>
            </div>
          ) : (
            <>
              {questions.map((q, i) => (
                <div key={i} style={styles.qCard}>
                  <div style={styles.qTitle}>❓ السؤال {i + 1}: {q.سؤال}</div>
                  <div style={styles.qAnswer}>
                    ✅ <strong>الجواب المثالي:</strong><br />{q.جواب}
                  </div>
                </div>
              ))}
              <div style={{ textAlign: "center", marginTop: "24px" }}>
                <button style={styles.btn} onClick={startSimulation}>
                  🎭 ابدا Simulation ديال المقابلة
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* SIMULATION */}
      {step === "simulation" && (
        <div style={styles.page} className="fade">
          <button style={styles.backBtn} onClick={() => setStep("interview")}>← رجوع</button>
          <div style={styles.sectionTitle}>🎭 Simulation المقابلة</div>

          <div style={styles.card}>
            <div style={styles.chatBox}>
              {simMessages.map((m, i) => (
                <div key={i} style={styles.bubble(m.role)}>{m.text}</div>
              ))}
              {loading && (
                <div style={styles.bubble("interviewer")}>
                  <span style={styles.dots}>كيكتب...</span>
                </div>
              )}
            </div>

            <div style={styles.inputRow}>
              <input
                style={{ ...styles.input, marginBottom: 0, flex: 1 }}
                placeholder="جاوب هنا بالدارجة..."
                value={userInput}
                onChange={e => setUserInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && sendSimMessage()}
              />
              <button
                style={{ ...styles.btn, padding: "14px 20px", borderRadius: "12px" }}
                onClick={sendSimMessage}
                disabled={loading}
              >
                ↑
              </button>
            </div>
          </div>

          <div style={{ textAlign: "center", marginTop: "16px" }}>
            <button style={styles.btnSecondary} onClick={() => setStep("home")}>
              🔄 ابدا من جديد
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
