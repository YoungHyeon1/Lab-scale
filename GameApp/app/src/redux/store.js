import { configureStore } from "@reduxjs/toolkit";
import gameStatsReducer from "./gameStatsSlice";

export const store = configureStore({
  reducer: {
    gameStats: gameStatsReducer,
  },
});
