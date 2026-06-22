from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Job


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

