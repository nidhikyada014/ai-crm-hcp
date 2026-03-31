import React, { useState } from "react";
import axios from "axios";

function App() {
  const [hcpName, setHcpName] = useState("");
  const [type, setType] = useState("");
  const [notes, setNotes] = useState("");
  const [result, setResult] = useState("");

  const [aiInput, setAiInput] = useState("");
  const [aiOutput, setAiOutput] = useState("");

  const API = "http://127.0.0.1:8000";

  // ✅ TOOL 1 (Log Interaction)
  const handleSubmit = async () => {
    try {
      const res = await axios.post(`${API}/log-interaction`, {
        hcp_name: hcpName,
        interaction_type: type,
        notes: notes,
      });

      setResult(JSON.stringify(res.data, null, 2));
    } catch (err) {
      console.error("Error:", err);
      setResult("Error while submitting interaction");
    }
  };

  // ✅ TOOL 2 (LangGraph Agent)
  const handleAI = async () => {
    try {
      const res = await axios.post(`${API}/agent`, {
        input: aiInput,
      });

      setAiOutput(JSON.stringify(res.data, null, 2));
    } catch (err) {
      console.error("AI Error:", err);
      setAiOutput("Error calling AI agent");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Log Interaction</h2>

      <input
        placeholder="HCP Name"
        value={hcpName}
        onChange={(e) => setHcpName(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Interaction Type"
        value={type}
        onChange={(e) => setType(e.target.value)}
      />
      <br /><br />

      <textarea
        placeholder="Notes"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
      />
      <br /><br />

      <button onClick={handleSubmit}>Submit</button>

      <pre>{result}</pre>

      <hr />

      <h2>AI Agent (LangGraph)</h2>

      <input
        placeholder="Enter AI input"
        value={aiInput}
        onChange={(e) => setAiInput(e.target.value)}
      />
      <br /><br />

      <button onClick={handleAI}>Run Agent</button>

      <pre>{aiOutput}</pre>
    </div>
  );
}

export default App;
