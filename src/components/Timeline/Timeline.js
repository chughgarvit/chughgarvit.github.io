import React from "react"

import {
    VerticalTimeline,
    VerticalTimelineElement
} from "react-vertical-timeline-component"

import "react-vertical-timeline-component/style.min.css"
import "./Timeline.css"
import { ReactComponent as WorkIcon } from "../../assets/work.svg"
import { ReactComponent as SchoolIcon } from "../../assets/school.svg"

import { education } from '../../portfolio'

const workIconStyles = { background: "#ffffff" };
const schoolIconStyles = { background: "#ffffff" };

const Timeline = () => {
    if (!education.length) return null

    return (
        <section id='timeline' className='section publications'>

            <div>
                <h2 className="education__title">Timeline</h2>
                <VerticalTimeline>
                    {education.map((element) => {
                        const isWorkIcon = element.icon === "work";


                        return (
                            <VerticalTimelineElement
                                key={element.key}
                                date={element.date}
                                dateClassName="date"
                                iconStyle={isWorkIcon ? workIconStyles : schoolIconStyles}
                                icon={isWorkIcon ? <WorkIcon /> : <SchoolIcon />}
                            >
                                <h3 className="vertical-timeline-element-title">
                                    {element.title}
                                </h3>
                                <h5 className="vertical-timeline-element-subtitle">
                                    {element.location}
                                </h5>
                                <p id="description">{element.description}</p>
                                {/* {showButton && (
                                    <a
                                        className={`button ${isWorkIcon ? "workButton" : "schoolButton"
                                            }`}
                                        href="/"
                                    >
                                        {element.buttonText}
                                    </a>
                                )} */}
                            </VerticalTimelineElement>
                        );
                    })}
                </VerticalTimeline>
            </div>
        </section>
    )
}

export default Timeline
