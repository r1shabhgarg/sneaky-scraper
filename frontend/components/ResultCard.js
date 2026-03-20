export default function ResultCard({ result }) {
  if (!result) return null

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">{result.title}</h1>
      </div>

      {/* Summary */}
      <div>
        <h2 className="text-xl font-semibold text-gray-800 mb-2">Summary</h2>
        <p className="text-gray-700 leading-relaxed">{result.summary}</p>
      </div>

      {/* Key Points */}
      {result.key_points && result.key_points.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-gray-800 mb-3">Key Points</h2>
          <ul className="space-y-2">
            {result.key_points.map((point, idx) => (
              <li key={idx} className="flex items-start gap-3">
                <span className="text-blue-600 font-bold mt-1">•</span>
                <span className="text-gray-700">{point}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Important Details */}
      {result.important_details && result.important_details.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-gray-800 mb-3">Important Details</h2>
          <ul className="space-y-2">
            {result.important_details.map((detail, idx) => (
              <li key={idx} className="flex items-start gap-3">
                <span className="text-green-600 font-bold mt-1">✓</span>
                <span className="text-gray-700">{detail}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
