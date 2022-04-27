import { Container, Row } from 'react-bootstrap'
import uniqid from 'uniqid'
import React from 'react'
import { pubs } from '../../portfolio'
import AchievementsContainer from '../AchievementsContainer/AchievementsContainer'
import './Achievements.css'


const Achievements = () => {
  if (!pubs.length) return null

  return (
    <section id='achievements' className='section achievements'>
      <h2 className='section__title'>Achievements</h2>

      <div className='achievements__grid'>
        <ul className='listItem'>
          <li>
            2022
          </li>
        </ul>
        <Container style={{ height: pubs.length * 50 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <AchievementsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>

        <ul className='listItem'>
          <li>
            2021
          </li>
        </ul>
        <Container style={{ height: pubs.length * 50 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <AchievementsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>


        <ul className='listItem'>
          <li>
            2020
          </li>
        </ul>
        <Container style={{ height: pubs.length * 50 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <AchievementsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>


        <ul className='listItem'>
          <li>
            2019
          </li>
        </ul>
        <Container style={{ height: pubs.length * 50 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <AchievementsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>


        <ul className='listItem'>
          <li>
            1998
          </li>
        </ul>
        <Container style={{ height: pubs.length * 50 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <AchievementsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>

      </div >
    </section >
  )
}

export default Achievements
