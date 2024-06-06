import SidebarComponent from "./SidebarComponent";
// import { SearchBar } from "./SearchBar";
import React, {useState} from "react";
import { useSelector } from "react-redux";
import styled from "styled-components";



const ImageContainer = styled.div`
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #000;
`;

const Image = styled.img`
  width: 100px;
  height: 100px;
  object-fit: cover;
`;
const CardContainer = styled.div`
  
  width: 100%;
`;

const Card = styled.div`
  background: #fff;
  width: 70%;
  justify-content: center;

`;

const CardHeader = styled.div`
  background: #007bff;
  color: #fff;
  padding: 0.5%;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  font-size: 1.2em;
`;

const CardBody = styled.div`
  padding: 10px;
`;

const CardTitle = styled.h3`
  margin: 0;
  font-size: 1.1em;
`;

const CardText = styled.p`
  margin: 5px 0;
  color: #555;
`;

const Research = () => {
   
    const [showModal, setShowModal] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const { stats } = useSelector((state) => state.gameStats);
    const handleSearchError = (message) => {
      setErrorMessage(message);
      setShowModal(true);
    };
    const handleClose = () => setShowModal(false);

    const sampleData = [
        { header: 'Header 1', title: 'Title 1', text: 'This is some sample text for card 1.' },
        { header: 'Header 2', title: 'Title 2', text: 'This is some sample text for card 2.' },
        { header: 'Header 3', title: 'Title 3', text: 'This is some sample text for card 3.' },
      ];
      
 
  
    return(
        <>
        <SidebarComponent />
        <div className="profile-bar">
            <img src="profile.jpg" alt="" className="profile-image" />
            <span className="profile-name">John Doe</span>
        </div>
        
        <CardContainer>
        {sampleData.map((item, index) => (
            <Card key={index}>
            <CardHeader>{item.header}</CardHeader>
            <CardBody>
                <CardTitle>{item.title}</CardTitle>
                <CardText>{item.text}</CardText>
            </CardBody>
            </Card>
        ))}
        </CardContainer>

        </>
    )
    
}

export default Research