import uniqid from 'uniqid'
import './AchievementsContainer.css'
import { Icon } from '@iconify/react';
import React from 'react';
import { Col, Container, Row } from 'react-bootstrap';
// import { ListSharp } from '@mui/icons-material';

const AchievementsContainer = ({ publication }) => (

  <Container key={uniqid()} data-aos='fade-up' data-aos-delay='100' className='achCard'>
    <Row className='textVerticalAlign'>
      <Col xs={1}>

        <Icon icon='bx:award' color='#79774C' />
      </Col>
      <Col xs={11} className='achNames'>
        {publication.head}
        <ul className='listStyle'>
          {publication.tail.map((data) => (
            <li>
              {data}
            </li>
          ))}
        </ul>
      </Col>
    </Row>
  </Container>
)

export default AchievementsContainer
