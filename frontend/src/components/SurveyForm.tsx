import React, { useState } from 'react';
import swal from 'sweetalert2';
import axios from 'axios';

// Define types for survey data
interface SurveyResult {
  question_number: number;
  question_value: number;
}

interface SurveyData {
  user_id: string;
  survey_results: SurveyResult[];
}

const SurveyForm: React.FC = () => {
  const [userId, setUserId] = useState<string>('');
  const [surveyResults, setSurveyResults] = useState<number[]>(Array(10).fill(0));
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const handleUserIdChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUserId(event.target.value);
  };

  const handleResponseChange = (index: number, value: number) => {
    setSurveyResults((prevResults) => {
      const updatedResults = [...prevResults];
      updatedResults[index] = value;
      return updatedResults;
    });
  };

  const validatePayload = (): boolean => {
    if (!/^[a-zA-Z0-9_]{5,20}$/.test(userId)) {
      swal.fire("Validation Error", "User ID must be 5-20 characters and can only contain letters, numbers, and underscores.", "error");
      return false;
    }

    if (surveyResults.length !== 10) {
      swal.fire("Validation Error", "There must be exactly 10 responses.", "error");
      return false;
    }

    for (let i = 0; i < surveyResults.length; i++) {
      const questionValue = surveyResults[i];
      if (questionValue < 1 || questionValue > 7) {
        swal.fire("Validation Error", `Question ${i + 1} value must be between 1 and 7.`, "error");
        return false;
      }
    }

    return true;
  };

  const handleSubmit = async (event?: React.FormEvent) => {
    event?.preventDefault();

    if (!validatePayload()) return;

    const surveyData: SurveyData = {
      user_id: userId,
      survey_results: surveyResults.map((value, index) => ({
        question_number: index + 1,
        question_value: value,
      })),
    };

    setIsSubmitting(true);

    try {
      const response = await axios.post('http://localhost:5050/process_survey', surveyData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.status === 200) {
        swal.fire("Success", `Survey submitted successfully! <br> <br> We Determined from this survey that <br> <br> <b> ${response.data.insights.description} </b>`, "success");
      } else {
        swal.fire("Error", "Failed to submit survey.", "error");
      }
    } catch (error) {
      console.error('Error submitting survey:', error);
      swal.fire("Error", "An error occurred while submitting the survey.", "error");
    } finally {
      setIsSubmitting(false);
      resetForm();
    }
  };

  const resetForm = () => {
    setUserId('');
    setSurveyResults(Array(10).fill(0));
  };

  const handleAutoGenerateAndSubmit = () => {
    setUserId(`user_${Math.random().toString(36).substring(2, 7)}`);
    setSurveyResults(Array.from({ length: 10 }, () => Math.floor(Math.random() * 7) + 1));
  };

  return (
    <form onSubmit={handleSubmit} className="container mt-4 p-4 border rounded bg-light">
      <h2 className="text-center mb-4">Survey Form</h2>

      <div className="mb-3">
        <label htmlFor="user-id" className="form-label">User ID</label>
        <input
          type="text"
          id="user-id"
          value={userId}
          onChange={handleUserIdChange}
          className="form-control"
          placeholder="Enter your user ID"
          required
          disabled={isSubmitting}
        />
      </div>

      {surveyResults.map((_, index) => (
        <div key={index} className="mb-3">
          <label htmlFor={`question-${index + 1}`} className="form-label">Question {index + 1}</label>
          <input
            type="number"
            id={`question-${index + 1}`}
            min="1"
            max="7"
            value={surveyResults[index]}
            onChange={(e) => handleResponseChange(index, Number(e.target.value))}
            className="form-control"
            placeholder="Enter a value between 1 and 7"
            required
            disabled={isSubmitting}
          />
        </div>
      ))}

      <div className="d-flex justify-content-between mt-4">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Submitting...' : 'Submit Survey'}
        </button>
        <button
          type="button"
          onClick={handleAutoGenerateAndSubmit}
          className="btn btn-secondary"
          disabled={isSubmitting}
        >
          Auto-Fill Survey Form
        </button>
      </div>
    </form>
  );
};

export default SurveyForm;
