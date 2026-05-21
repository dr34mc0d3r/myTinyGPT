# Loss Curve & Training Log Analysis

Monitoring training logs is critical for diagnosing model performance and debugging training instabilities in `myTinyGPT`. This guide consolidates essential resources and best practices for interpreting training dynamics.

## 1. Key Resources
- **[Andrej Karpathy's "A Recipe for Training Neural Networks"](https://karpathy.github.io/2019/04/25/notebook/):** The gold standard for understanding loss curves, spotting under/overfitting, and tuning hyperparameters.
- **[Weights & Biases (W&B) "Debugging Neural Networks"](https://wandb.ai/site/articles/debugging-neural-networks):** Provides visual guides on healthy vs. unhealthy training dynamics.
- **[TensorBoard Documentation](https://www.tensorflow.org/tensorboard/get_started):** Essential for learning how to visualize and log metrics effectively.
- **[PyTorch Lightning "Logging Best Practices"](https://lightning.ai/docs/pytorch/stable/extensions/logging.html):** Offers a standard engineering baseline for production-quality logging (what to log, when, and why).

## 2. Technical Concepts for Debugging
When investigating anomalies in your logs, focus on these phenomena:
- **Loss Plateauing:** The point where loss stops decreasing; indicates need for hyperparameter adjustment (LR, batch size) or more data.
- **Divergence / Exploding Gradients:** Loss spikes unexpectedly to `NaN` or infinity. Often caused by too high a learning rate or lack of gradient clipping.
- **Overfitting vs. Underfitting:** Discrepancies between training and validation loss curves.
- **Learning Rate Sensitivity:** How LR interacts with batch size and weight decay to affect training stability.

## 3. Recommended Metrics for `myTinyGPT`
To improve diagnostic capability beyond just logging `loss`, ensure your `ai_system/app/training/trainer.py` captures:

| Metric | Purpose |
| :--- | :--- |
| **Learning Rate** | Monitor adherence to the warmup and decay schedule. |
| **Gradient Norms** | Detects exploding gradients before they cause `NaN` loss. |
| **Weight Distributions** | Helps identify "dying neurons" (weights collapsing to zero). |
| **Throughput (iter/sec)** | Ensures training efficiency remains stable as the model grows. |

### 3.1 Training Terminology Explained

| Term | Definition | Why It Matters |
| :--- | :--- | :--- |
| **Iteration (iter)** | A single processing step where the model sees one batch of data. | Measures progress; higher iteration counts usually mean better training. |
| **Loss** | A mathematical value representing how "wrong" the model's predictions are. | Your primary indicator of learning. Lower is better; it should trend down. |
| **Time (ms)** | The duration the current batch took to process (in milliseconds). | Used to identify bottlenecks; slower times suggest hardware or code complexity issues. |
| **Learning Rate (lr)** | A hyperparameter that controls how much the model's weights change. | Too high = training unstable; too low = model learns too slowly. |

### 3.2 Monitoring Growth: What to Look For
As your training list grows, keep these indicators in mind:

1.  **Consistent Loss Decrease**: The loss should drop rapidly at first and then settle into a slower, steady decline. If it stops decreasing (plateaus), the model has likely stopped learning.
2.  **Stable Training Time**: Processing time per iteration should remain relatively consistent. If it jumps significantly, it could indicate background resource contention or memory issues.
3.  **Dynamic LR**: You should see your learning rate (lr) increase during the "warmup" phase and then decrease during the "decay" phase. This is intentional and optimal for convergence.
4.  **Avoid Plateau/Divergence**: If the loss suddenly spikes, the model is diverging. Check your learning rate—it might be set too high for the current training stability.

---

## 4. Reference: Training Manual (Loss Curve Analysis)

*The following content provides a comprehensive framework for diagnosing neural network health using loss curves.*

### A. What is "Loss"?
Loss is the model’s error score that the optimizer attempts to minimize. Common loss functions include `CrossEntropyLoss` (classification/sequence models) and `MSELoss` (regression).

### B. Healthy Loss Curve Characteristics
- Training loss decreases steadily.
- Validation loss also decreases.
- Validation loss remains close to the training loss.

### C. Troubleshooting Guide: Reading Curves Like an Engineer

| Pattern | Diagnosis | Potential Fixes |
| :--- | :--- | :--- |
| **Train ↓, Val ↑** | Overfitting | Dropout, weight decay, data augmentation, early stopping, smaller model. |
| **Train High, Val High** | Underfitting | Larger model, train longer, better optimizer, better data. |
| **Loss Explodes** | Divergence / Exploding Gradients | Gradient clipping (`clip_grad_norm_`), lower LR, better normalization. |
| **Loss Oscillates** | Unstable Training | Scheduler adjustment, gradient clipping, check batch size. |
| **Flat Curve** | Not Learning | Adjust learning rate (check LR schedule), check model architecture. |

### D. Advanced Diagnostics
- **Batch vs. Epoch Loss:** Batch loss is noisy but useful for detecting immediate gradient issues; epoch loss is smoothed and ideal for trend/overfitting analysis.
- **Smoothing Noisy Curves:** Use moving averages (e.g., `np.convolve`) to clarify noisy batch logs.
- **Early Stopping:** Essential to save time and prevent overfitting. Stop when validation loss fails to improve for a set `patience` period.
- **LR Effects:**
  - **Too High:** Wild oscillations.
  - **Too Low:** Painfully slow decrease.
  - **Optimal:** Smooth downward curve.
- **Classification Nuance:** Accuracy can improve while loss worsens if the model becomes "more confidently wrong" on failures. Always monitor loss as a primary indicator of convergence.

### E. Professional Workflow Recommendation
1.  **Plot:** Visualize both train and validation loss.
2.  **Identify:** Diagnose based on the table above.
3.  **Adjust:** Change **ONE** variable at a time (e.g., just the learning rate).
4.  **Retrain:** Compare curves to verify the impact.

---
*Regularly review your TensorBoard logs for these metrics to ensure the model is converging correctly.*
