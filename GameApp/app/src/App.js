import React from "react";
import { Provider } from "react-redux";
import { store } from "./redux/store";
import MainPage from "./components/MainPage";
import GlobalStyle from "./components/GlobalStyle"; // 스타일링을 위한 글로벌 스타일
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Research from "./components/Research";
function App() {
  return (
    <Router>
      <Provider store={store}>
        <GlobalStyle />
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/about" element={<Research />} />

        </Routes>
      </Provider>

    </Router>
    
  );
}

export default App;
