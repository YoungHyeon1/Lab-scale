import { configureStore } from "@reduxjs/toolkit";
import getPuuidSliceReducer from "./getPuuidSlice";
import userLeagueSlice from "./userLeagueSlice";

export const store = configureStore({
  reducer: {
    getPuuid: getPuuidSliceReducer,
    userLeague: userLeagueSlice,
  },
});
