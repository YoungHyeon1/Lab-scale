import React from "react";
import { Provider } from "react-redux";
import { store } from "./redux/store";
import MainPage from "./components/MainPage";
import GlobalStyle from "./components/GlobalStyle"; // 스타일링을 위한 글로벌 스타일
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Research from "./components/Research";
import CardList from "./components/testcomponent";
import AIPredicPage from "./components/AIPredicPage";

function App() {
  return (
    <Router>
      <Provider store={store}>
        <GlobalStyle />
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/research/:gameName" element={<Research />} />
          <Route path="/cards" element={<CardList />} />
          <Route path="/ai_search" element={<AIPredicPage />} />
          {/* CardList 라우트 추가 */}
        </Routes>
      </Provider>
    </Router>
  );
}

export default App;
