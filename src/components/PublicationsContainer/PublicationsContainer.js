import uniqid from 'uniqid'
// import GitHubIcon from '@material-ui/icons/GitHub'
import LaunchIcon from '@material-ui/icons/Launch'
import './PublicationsContainer.css'
import { Icon } from '@iconify/react';
import React from "react";
import { Col, Container, Row } from 'react-bootstrap';
// import WorkspacePremiumIcon from '@mui/icons-material/WorkspacePremium';
// import { AccessAlarm, ThreeDRotation } from '@mui/icons-material';


const PublicationsContainer = ({ publication }) => (

  <Container key={uniqid()} data-aos="fade-up" data-aos-delay="100" className="pubCard">
    <Row style={{ height: 50 }} className="textVerticalAlign">
      <Col xs={1}>

        <Icon icon="bx:award" color="#79774C" width="20px" height="20px" />
      </Col>
      <Col xs={9} className="pubNames">
        {publication.name}
      </Col>
      <Col xs={2}>
        {publication.link && (
          <a
            href={publication.link}
            aria-label='live preview'
            className='link link--icon'
          >
            <LaunchIcon />
          </a>
        )}
      </Col>
    </Row>
    <Row className="authNames textVerticalAlign" style={{ height: 20 }}>
      <Col xs={1} />
      <Col>
        {publication.authors}
      </Col>
    </Row>
    <Row style={{ height: 10 }} />
  </Container>
)

export default PublicationsContainer
