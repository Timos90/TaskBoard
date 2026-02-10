/**
 * TaskCard - Individual task display component
 * 
 * Displays a task with title, description, and optional delete button.
 * Clickable to edit if onEdit callback is provided.
 * 
 * @param {Object} task - Task object with id, title, description
 * @param {Function} onEdit - Optional callback when task is clicked (for editing)
 * @param {Function} onDelete - Optional callback when delete button is clicked
 */
function TaskCard({task, onEdit, onDelete}) {
    const canEdit = !!onEdit
    const canDelete = !!onDelete

    return <div
        className={`task-card ${canEdit ? 'task-card-clickable' : ""}`}
        onClick={canEdit ? () => onEdit(task) : undefined}
    >
        <div className={"task-card-header"}>
            <h4 className={"task-card-title"}>{task.title}</h4>
            {canDelete && (
                <button
                    className={"task-card-btn task-card-btn-delete"}
                    onClick={(e) => {
                        e.stopPropagation()
                        onDelete(task.id)
                    }}
                    title={"Delete Task"}
                >
                    x
                </button>
            )}
        </div>
        {task.description && (
            <p className={"task-card-description"}>{task.description}</p>
        )}
    </div>
}

export default TaskCard