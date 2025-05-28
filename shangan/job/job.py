from dataclasses import dataclass, field

@dataclass
class JobRequirement:
    xuewei: str
    xueli: str
    min_work_year: str
    max_age: str
    work_experience: str
    skill: str
    other: str = field(default_factory=str)


@dataclass
class JobInfo:
    job_id: str
    description: str
    name: str
    department: str
    unit: str
    job: str
    num: int

@dataclass
class JobRecruitment:
    job_id: str
    requirements: JobRequirement
    description: JobInfo

