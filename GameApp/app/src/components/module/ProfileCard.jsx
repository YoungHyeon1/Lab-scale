import React from "react";
import styled from "styled-components";

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
);

export default ProfileCard;
