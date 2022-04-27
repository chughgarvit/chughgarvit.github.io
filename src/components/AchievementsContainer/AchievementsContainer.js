import uniqid from 'uniqid'
import './AchievementsContainer.css'
import { Icon } from '@iconify/react';
import React from "react";
import { Col, Container, Row } from 'react-bootstrap';

const AchievementsContainer = ({ publication }) => (

  <Container key={uniqid()} data-aos="fade-up" data-aos-delay="100" className="achCard">
    <Row style={{ height: 30 }} className="textVerticalAlign">
      <Col xs={1}>

        <Icon icon="bx:award" color="#79774C" width="20px" height="20px" />
      </Col>
      <Col xs={11} className="achNames">
        {publication.name}
      </Col>
    </Row>
  </Container>
)

export default AchievementsContainer
