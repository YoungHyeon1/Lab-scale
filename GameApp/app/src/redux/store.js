import { configureStore } from "@reduxjs/toolkit";
import getPuuidSliceReducer from "./getPuuidSlice";
import userLeagueSlice from "./userLeagueSlice";
import matchesInfoReducer from "./matchSlice";
import recordSliceReducer from "./updateMatchSlice";

export const store = configureStore({
  reducer: {
    getPuuid: getPuuidSliceReducer,
    userLeague: userLeagueSlice,
    match: matchesInfoReducer,
    record: recordSliceReducer,
  },
});
