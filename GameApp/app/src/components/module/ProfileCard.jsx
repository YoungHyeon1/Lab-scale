import React from "react";
import styled from "styled-components";



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

const LevelBadge = styled.div`
  background-color: #191919;
  color: white;
  padding: 3px 8px;
  border-radius: 15px;
  font-size: 12px;
`;

const ButtonContainer = styled.div`
  margin-top: 20px;
`;

const UpdateButton = styled.button`
  background-color: #1f8ecd; // 예시 버튼 색상
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
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

const ProfileCard = ({ profile }) => (
  <ProfileContainer>
    <LeftSection>
      <ProfileImage src={profile.imageUrl} alt="profile" />
      <SummonerInfo>
        <SummonerName>{profile.name}</SummonerName>
        <LevelBadge>Lv. {profile.level}</LevelBadge>
      </SummonerInfo>
      <ButtonContainer>
        <UpdateButton>전적 갱신</UpdateButton>
        <LastUpdated>최근 업데이트: {profile.lastUpdated}</LastUpdated>
      </ButtonContainer>
      {/* 백엔드에서 받아올 텍스트 정보 표시 */}
    </LeftSection>
    <RightSection>
      <RankIcon src={profile.rankIconUrl} alt="rank icon" />
      <RankText>{profile.tier} {profile.division}</RankText>
      <WinLoss>{profile.wins}승 {profile.losses}패 ({profile.winRate}%)</WinLoss>
    </RightSection>
  </ProfileContainer>
);
/*
const ProfileContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f3f4f6;
  padding: 20px;
  border-radius: 10px;
  margin: 20px;
`;

const ProfileCard = ({ profile }) => (
  <ProfileContainer>
    <img
      src={profile.imageUrl}
      alt="profile"
      style={{ width: "100px", height: "100px", borderRadius: "50%" }}
    />
    <h2>{profile.name}</h2>
    <p>{profile.rank}</p>
  </ProfileContainer>
);*/

export default ProfileCard;
