import React, { useEffect, useRef } from "react";
import styled from "styled-components";
import { useDispatch, useSelector } from "react-redux";
import { useState } from "react";
import {
  updateRecord,
  pollTaskStatus,
  stopPolling,
} from "../../redux/updateMatchSlice";

const ProfileContainer = styled.div`
  display: flex;
  background: #e4e4e4;
  border-radius: 10px;
  width: 70%; // 전체 프로필 카드 너비
  margin: 20px auto;
  border: 1px solid #d6d6d6;
  overflow: hidden; // 자식 요소가 넘칠 경우 숨김
`;

const LeftSection = styled.div`
  flex: 7; // 70% 비율
  padding: 20px;
  display: flex;
  flex-direction: column;
`;

const ProfileImage = styled.img`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 10px;
`;

const SummonerInfo = styled.div`
  display: flex;
  align-items: center;
`;

const SummonerName = styled.div`
  font-size: 18px;
  font-weight: bold;
  margin-right: 10px;
`;

const TagName = styled.div`
  font-size: 18px;
  font-weight: bold;
  margin-right: 10px;
  color: #bdbdbd;
`;

const LevelBadge = styled.div`
  background-color: #191919;
  color: white;
  padding: 3px 8px;
  width: 50px;
  border-radius: 15px;
  font-size: 12px;
`;

const ButtonContainer = styled.div`
  margin-top: 20px;
`;

const UpdateButton = styled.button`
  background-color: #1f8ecd;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;

  &:disabled {
    background-color: #ccc; // disabled 상태일 때 배경색 변경
    cursor: default; // disabled 상태일 때 커서 변경
  }
`;
const LastUpdated = styled.div`
  font-size: 12px;
  color: #555;
  margin-top: 10px;
`;

const RightSection = styled.div`
  flex: 3; // 30% 비율
  background-color: #f0f0f0; // 밝은 회색 배경
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const RankIcon = styled.img`
  width: 50px;
  height: 50px;
  margin-bottom: 10px;
`;

const RankText = styled.div`
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
`;

const WinLoss = styled.div`
  font-size: 14px;
  color: #555;
`;

const ProfileCard = ({ profile }) => {
  const dispatch = useDispatch();
  const { loading, is_complete, task_id, isPolling, error } = useSelector(
    (state) => state.record
  );
  const [complet, setComplete] = useState(false);
  const result = useSelector((state) => state.getPuuid.result);
  const pollingRef = useRef(null);

  const handleUpdateRecord = () => {
    console.log(complet, task_id);
    dispatch(updateRecord(result.puuid));
  };
  useEffect(() => {
    setComplete(isPolling);
    console.log(isPolling);
    if (task_id && !is_complete && !pollingRef.current) {
      pollingRef.current = setInterval(() => {
        console.log(isPolling);
        dispatch(pollTaskStatus(task_id));
      }, 5000); // 5초 간격
    }
    if (is_complete && pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
      dispatch(stopPolling()); // 상태 정리
    }
    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
    };
  }, [dispatch, task_id, is_complete, isPolling]);

  // 에러 감지
  useEffect(() => {
    if (error) {
      alert("Error occurred: " + error);
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
        pollingRef.current = null;
      }
    }
  }, [error]);
  return (
    <ProfileContainer>
      <LeftSection>
        <ProfileImage src={profile.imageUrl} alt="profile" />
        <SummonerInfo>
          <SummonerName>{profile.name}</SummonerName>
          <TagName>{profile.tag}</TagName>
        </SummonerInfo>
        <LevelBadge>Lv. {profile.level}</LevelBadge>
        <ButtonContainer>
          <UpdateButton onClick={handleUpdateRecord} disabled={complet}>
            전적 갱신
          </UpdateButton>
          <LastUpdated>
            최근 업데이트: {profile.lastUpdated.split("T")[0]}
          </LastUpdated>
        </ButtonContainer>
        {/* 백엔드에서 받아올 텍스트 정보 표시 */}
      </LeftSection>

      {profile.leagues.map((league, index) => (
        <RightSection key={index}>
          <RankIcon src={league.rankIconUrl} alt="rank icon" />
          <RankText>
            {league.tier} {league.division}
          </RankText>
          <WinLoss>
            {league.wins}승 {league.losses}패 ({league.winRate}%)
          </WinLoss>
          <RankText>{league.queue_type}</RankText>
        </RightSection>
      ))}
    </ProfileContainer>
  );
};

export default ProfileCard;
