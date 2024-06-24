// features/recordSlice.js
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const updateRecord = createAsyncThunk(
  "record/updateRecord",
  async (puuid, {dispatch, rejectWithValue }) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/v1/match/update?user_id=${puuid}`
      );
      dispatch(pollTaskStatus(response.data.task_id));
      return response.data; // { service_name, task_id }
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const pollTaskStatus = createAsyncThunk(
  "record/pollTaskStatus",
  async (task_id, { rejectWithValue }) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/v1/match/status?task_id=${task_id}`
      );
      return response.data; // { status, service_name, is_complete }
    } catch (error) {
      return rejectWithValue(error);
    }
  }
);

const recordSlice = createSlice({
  name: "record",
  initialState: {
    loading: false,
    error: null,
    task_id: null,
    service_name: null,
    status: null,
    is_complete: false,
    isPolling: false,
  },
  reducers: {
    stopPolling(state) {
      state.isPolling = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(updateRecord.pending, (state) => {
        state.loading = true;
      })
      .addCase(updateRecord.fulfilled, (state, action) => {
        state.loading = false;
        state.task_id = action.payload.task_id;
        state.service_name = action.payload.service_name;
      })
      .addCase(updateRecord.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(pollTaskStatus.fulfilled, (state, action) => {
        state.status = action.payload.status;
        state.is_complete = action.payload.is_complete;
        if (action.payload.is_complete) {
          state.isPolling = false;
        } else {
          state.isPolling = true;
        }
      })
      .addCase(pollTaskStatus.rejected, (state, action) => {
        state.error = action.payload;
        state.isPolling = false;
      });
  },
});

export const { stopPolling } = recordSlice.actions;
export default recordSlice.reducer;
