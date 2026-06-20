import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Job
from database import async_session_maker

class JobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(self):
        query = select(Job)
        results = await self.session.execute(query)
        return results.scalars().all()


    async def get_by_id(self, job_id: int):
        query = select(Job).where(Job.id == job_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def create(self, job_instance: Job):
        self.session.add(job_instance)
        await self.session.commit()
        await self.session.refresh(job_instance)
        return job_instance


    async def update(self, job_id: int, update_data: dict):
        db_job = await self.get_by_id(job_id)
        if db_job is None:
            return None

        for k,v in update_data.items():
            if hasattr(db_job, k):
                setattr(db_job, k, v)

        await self.session.commit()
        await self.session.refresh(db_job)
        return db_job


    async def delete(self, job_id: int):
        db_job = await self.get_by_id(job_id)
        if db_job is None:
            return False

        await self.session.delete(db_job)
        await  self.session.commit()
        return True




async def test_get_all():
    async with async_session_maker() as session:
        repo = JobRepository(session)
        jobs = await repo.get_all()
        print(jobs)


async def test_get_by_id(id):
    async with async_session_maker() as session:
        repo = JobRepository(session)
        jobs = await repo.get_by_id(id)
        print(jobs)


async def test_create(data):
    async with async_session_maker() as session:
        repo = JobRepository(session)
        jobs = await repo.create(data)
        print(jobs)


async def test_update(id, data):
    async with async_session_maker() as session:
        repo = JobRepository(session)
        jobs = await repo.update(id, data)
        print(jobs)


async def test_delete(id):
    async with async_session_maker() as session:
        repo = JobRepository(session)
        jobs = await repo.delete(id)
        print(jobs)



data_job = Job(
    title="Python Developer",
    description="Junior backend",
    salary=1200
)
data_job2 = {
    "description": "Bizga Pythonda fast api da mustaqil kod yoza oladigan  senior developer kerak",
    "title": "Backend developer",
    "salary": 5000
}




async def main():
    await test_get_all()
    await  test_create(data_job)
    await  test_get_by_id(2)
    await  test_update(2, data_job2)
    await  test_get_by_id(2)
    await  test_delete(2)
    await  test_get_by_id(2)

asyncio.run(main())   