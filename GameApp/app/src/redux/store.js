import { configureStore } from "@reduxjs/toolkit";
import getPuuidSliceReducer from "./getPuuidSlice";
import userInfoReducer from "./userInfoSlice";

export const store = configureStore({
  reducer: {
    getPuuid: getPuuidSliceReducer,
    userInfo: userInfoReducer,
  },
});
