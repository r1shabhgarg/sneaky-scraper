export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-4 border-gray-200"></div>
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-600 animate-spin"></div>
      </div>
      <p className="mt-4 text-gray-600 font-medium">Searching and processing...</p>
      <p className="text-sm text-gray-500 mt-1">This may take a moment</p>
    </div>
  )
}
