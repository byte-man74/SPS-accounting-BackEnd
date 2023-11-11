from Main.models import Payroll
BATCH_SIZE = 100



def process_salary_payment(payroll_id):
    payroll_instance = Payroll.objects.get(id=payroll_id)

    payroll_staffs = payroll_instance.staffs 
    num_batches = (payroll_staffs.count() + BATCH_SIZE - 1) // BATCH_SIZE

    # Create and return batches
    batches = [payroll_staffs[i * BATCH_SIZE:(i + 1) * BATCH_SIZE] for i in range(num_batches)]

    print(batches)
