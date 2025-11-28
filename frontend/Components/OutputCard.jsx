import { useState } from "react"

export default function OutputCard({ panel }) {
  const [isCopied, setIsCopied] = useState(false)

  const copyToClipboard = () => {
    navigator.clipboard.writeText(panel.content)
    setIsCopied(true)
    setTimeout(() => setIsCopied(false), 2000)
  }

  return (
    <div className="output-card">
      <div className="output-card-header">
        <div className="output-card-title-group">
          <span className="output-card-icon">{panel.icon}</span>
          <div>
            <h3 className="output-card-title">{panel.title}</h3>
            <p className="output-card-description">{panel.description}</p>
          </div>
        </div>
        <button onClick={copyToClipboard} className="copy-button" title="Copy to clipboard">
          {isCopied ? "✓" : "📋"}
        </button>
      </div>
      <pre className="output-card-content">
        <code>{panel.content || "Run code to see output"}</code>
      </pre>
    </div>
  )
}
