import { Container, Row } from 'react-bootstrap'
import uniqid from 'uniqid'
import React from 'react'
import { achievements2022, achievements2021, achievements2020, achievements2019, achievements2018 } from '../../pubPortfolio'
import AchievementsContainer from '../AchievementsContainer/AchievementsContainer'
import './Achievements.css'


const Achievements = () => (
  <section id='achievements' className='section achievements'>
    <h2 className='section__title'>Achievements</h2>

    <div className='achievements__grid'>

      {/* Year 2022 */}
      <ul className='listItem'>
        <li>
          2022
        </li>
      </ul>
      <Container style={{ height: achievements2022.length * 50 }}>
        {achievements2022.map((publication) => (
          <div>
            <Row>
              <AchievementsContainer key={uniqid()} publication={publication} />
            </Row>
            <Row style={{ height: 20 }} />
          </div>
        ))}
      </Container>

      {/* Year 2021 */}
      <ul className='listItem'>
        <li>
          2021
        </li>
      </ul>
      <Container style={{ height: achievements2021.length * 50 }}>
        {achievements2021.map((publication) => (
          <div>
            <Row>
              <AchievementsContainer key={uniqid()} publication={publication} />
            </Row>
            <Row style={{ height: 20 }} />
          </div>
        ))}
      </Container>

      {/* Year 2020 */}
      <ul className='listItem'>
        <li>
          2020
        </li>
      </ul>
      <Container style={{ height: achievements2020.length * 50 }}>
        {achievements2020.map((publication) => (
          <div>
            <Row>
              <AchievementsContainer key={uniqid()} publication={publication} />
            </Row>
            <Row style={{ height: 20 }} />
          </div>
        ))}
      </Container>


      {/* Year 2019 */}
      <ul className='listItem'>
        <li>
          2019
        </li>
      </ul>
      <Container style={{ height: achievements2019.length * 50 }}>
        {achievements2019.map((publication) => (
          <div>
            <Row>
              <AchievementsContainer key={uniqid()} publication={publication} />
            </Row>
            <Row style={{ height: 20 }} />
          </div>
        ))}
      </Container>


      {/* Year 2018 */}
      <ul className='listItem'>
        <li>
          1998
        </li>
      </ul>
      <Container style={{ height: achievements2018.length * 50 }}>
        {achievements2018.map((publication) => (
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

export default Achievements
