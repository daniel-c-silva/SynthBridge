import Main from "./components/main"; // 1. Fix the import name and path
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <Main /> {/* 2. Replace the header content with your component */}
    </div>
  );
}

export default App;
