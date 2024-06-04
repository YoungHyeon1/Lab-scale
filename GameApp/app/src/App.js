import React from "react";
import { Provider } from "react-redux";
import { store } from "./redux/store";
import MainPage from "./components/MainPage";
import GlobalStyle from "./components/GlobalStyle"; // 스타일링을 위한 글로벌 스타일

function App() {
  return (
    <Provider store={store}>
      <GlobalStyle />
      <MainPage />
    </Provider>
  );
}

export default App;
