import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const generateVideo = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/generate-video/", {
        prompt: prompt
      });

      const url = "http://localhost:8000" + response.data.video_path;
      setVideoUrl(url);
    } catch (error) {
      console.error("Generation failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App" style={{ padding: 30 }}>
      <h2>Text to Video Generator</h2>
      <input
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your prompt"
        style={{ width: "300px", padding: "8px" }}
      />
      <button onClick={generateVideo} style={{ marginLeft: "10px" }}>
        Generate
      </button>

      {loading && <p>Generating video...</p>}

      {videoUrl && (
        <div style={{ marginTop: 20 }}>
          <video width="480" controls>
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}

export default App;
