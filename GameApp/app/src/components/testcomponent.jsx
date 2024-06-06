import React, {useState} from "react";
import { useSelector } from "react-redux";
import styled, { keyframes } from "styled-components";
import SidebarComponent from "./SidebarComponent";
import SearchBar from "./SearchBar";


const ModalImageContainer = styled.div`
  width: 150px; /* 이미지 너비 고정 */
  height: 200px; /* 이미지 높이 고정 */
  margin-right: 20px; /* 이미지와 텍스트 간 간격 */
  overflow: hidden; /* 이미지가 컨테이너를 넘어가지 않도록 설정 */
`;

const ModalImage = styled.img`
  width: 100%;
  height: auto;
`;

const ModalTextContainer = styled.div`
  flex: 1; /* 텍스트 컨테이너가 남은 공간을 모두 차지하도록 설정 */
`;

const ModalText = styled.p`
  margin-bottom: 10px;
`;

const ModalLeftContainer = styled.div`
  width: 150px; /* 이미지 너비 고정 */
  margin-right: 20px; /* 이미지와 텍스트 간 간격 */
  overflow: hidden;
`;

const ModalRightContainer = styled.div`
  flex: 1; /* 텍스트 컨테이너가 남은 공간을 모두 차지하도록 설정 */
  display: flex;
  flex-direction: column;
`;


// 스핀 애니메이션 정의
const spin = keyframes`
  from {
    --rotate: 0deg;
  }
  to {
    --rotate: 360deg;
  }
`;




const CardContainer = styled.div`
  display: flex; /* flexbox 사용 */
  flex-wrap: wrap; /* 줄바꿈 설정 */
  gap: 20px; /* 카드 간 간격 설정 */
  padding: 20px;
  align-items: center;
  overflow-x: hidden; /* 가로 스크롤 숨김 */
  width: 100%; /* 화면 너비에 맞춤 */
  max-width: 800px; /* 최대 너비 제한 */
`;

const Card = styled.div`
  background: #191c29;
  width: calc(20% - 20px); /* 카드 너비 설정 (25% - 간격) */
  margin: 0 10px 20px 10px; /* 카드 간 간격 설정 */
  padding: 3px;
  position: relative;
  border-radius: 6px;
  display: flex;
  align-items: center;
  text-align: center;
  font-size: 1.0em;
  color: rgb(88 199 250 / 0%);
  cursor: pointer;
  font-family: cursive;
  transition: color 1s; // 마우스 호버 시 색 변화를 위한 트랜지션 추가
  --card-height: 250px; /* 카드 높이 증가 */

  &:hover {
    color: rgb(88 199 250 / 100%);
  }

  &:before, &:after {
    content: '';
    position: absolute;
    border-radius: 8px;
    z-index: -1;
    background-image: linear-gradient(var(--rotate), #5ddcff, #3c67e3 43%, #4e00c2);
    animation: ${spin} 2.5s linear infinite; // 스핀 애니메이션 적용
  }

  &:before { /* 바깥쪽 빛 효과 */
    width: 104%;
    height: 102%;
    top: -1%;
    left: -2%;
  }

  &:after { /* 안쪽 블러 효과 */
    top: calc(var(--card-height) / 6);
    left: 0;
    right: 0;
    height: 100%;
    width: 100%;
    margin: 0 auto;
    transform: scale(0.8);
    filter: blur(calc(var(--card-height) / 6));
    opacity: 1;
    transition: opacity 0.5s;
  }

  &:hover:before, &:hover:after { /* 호버 시 애니메이션과 투명도 제거 */
    animation: none;
    opacity: 0;
  }
`;

const ContentContainer = styled.div`
  flex: 3;
  padding: 20px;
`;

const CardTitle = styled.img`
  width: 10%;
  height: 20%;
  padding: 20px;
`;

const CardText = styled.p`
  margin: 10px 0 0;
  color: #FFFF;
  font-size: 0.8em; /* 폰트 크기 감소 */
  line-height: 1.2; /* 줄 간격 조절 */
`;

// Modal 스타일 컴포넌트
const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); // 어두운 배경
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 다른 요소 위에 표시 */
`;

const ModalContent = styled.div`
  background-color: white; /* 배경색 흰색 유지 */
  padding: 20px;
  border-radius: 5px;
  width: 500px; /* 모달 너비 조절 */
  height: 200px; /* 모달 높이 조절 */
  display: flex; /* flexbox 사용 */
  position: relative; /* 닫기 버튼 위치 설정 */
`;

const CloseButton = styled.button`
  position: absolute;
  top: 7px;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: white;
  border: 1px solid black;
  color: black;
  padding: 3px 5px;
  border-radius: 2px;
`;

const sampleData = [
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 1' },
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 2' },
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 1' },
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 1' },
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 1' },
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 1' },
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 1' },
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 1' },
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 1' },
  { text : 'KDA', text2: '몇 시간 전 플레이', imageUrl: '이미지 URL 1' },
];



// CardList 컴포넌트 수정
const CardList = () => {
  const [showModal, setShowModal] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const { stats } = useSelector((state) => state.gameStats);
  const [selectedCard, setSelectedCard] = useState(null);

  const handleSearchError = (message) => {
    setErrorMessage(message);
    setShowModal(true);
  };

  const handleCardClick = (item) => {
    setSelectedCard(item);
  };

  const handleCloseModal = () => {
    setSelectedCard(null);
  };

  return (
    <>
      <SearchBar onSearch={''} onError={handleSearchError} />
      <CardContainer>
        <SidebarComponent />
        {sampleData.map((item, index) => (
          <Card key={index} style={{ "--card-width": "calc(20% - 20px)", "--card-height": "250px" }} onClick={() => handleCardClick(item)}>
            <ContentContainer>
          
              <CardText>{item.text1}</CardText>
              <CardText>{item.text2}</CardText>
            </ContentContainer>
          </Card>
        ))}
      </CardContainer>

      {showModal && (
        <ModalOverlay>
          <ModalContent>
            <p>{errorMessage}</p>
            <button onClick={() => setShowModal(false)}>닫기</button>
          </ModalContent>
        </ModalOverlay>
      )}

      {selectedCard && (
        <ModalOverlay>
          <ModalContent>
            <CloseButton onClick={handleCloseModal}>X</CloseButton>
            <ModalLeftContainer>
              <ModalImage src={selectedCard.imageUrl} alt="Modal Image" />
            </ModalLeftContainer>
            <ModalRightContainer>
              <ModalText>{selectedCard.title}</ModalText>
              <ModalText>{selectedCard.text1}</ModalText>
              <ModalText>{selectedCard.text2}</ModalText>
              {/* 필요에 따라 추가 텍스트 컴포넌트 추가 */}
            </ModalRightContainer>
          </ModalContent>
        </ModalOverlay>
      )}
    </>
  );
};


export default CardList;
