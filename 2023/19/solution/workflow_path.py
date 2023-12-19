from solution.part_range import PartRange


class WorkflowPath:
    def __init__(self, next_workflow: str, part_range: PartRange):
        self.next_workflow = next_workflow
        self.part_range = part_range
