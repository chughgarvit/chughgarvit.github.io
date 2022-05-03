import { Container, Row } from 'react-bootstrap'
import uniqid from 'uniqid'
import React from 'react'
import { achievements } from '../../pubPortfolio'
import AchievementsContainer from '../AchievementsContainer/AchievementsContainer'
import './Achievements.css'


const Achievements = () => (
  <section id='achievements' className='section achievements'>
    <h2 className='section__title'>Achievements</h2>

    <div className='achievements__grid'>

      {achievements.map((achievement) => (
        <div>
          <ul className='listItem'>
            <li>
              {achievement.year}
            </li>
          </ul>
          <Container >
            {achievement.data.map((publication) => (
              <div>
                <Row>
                  <AchievementsContainer key={uniqid()} publication={publication} />
                </Row>
              </div>
            ))}
          </Container>
        </div>
      ))}
    </div >
  </section >
)

export default Achievements
