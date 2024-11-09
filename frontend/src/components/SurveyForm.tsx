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
  const [responses, setResponses] = useState<any[]>([]);

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
        headers: { 'Content-Type': 'application/json' },
      });

      if (response.status === 200) {
        const responseData = response.data.insights;
        if(responses.length === 10){
          setResponses([responseData, ...responses.slice(0, 9)]);
        }
        setResponses([responseData, ...responses]);
        swal.fire("Success", "Survey submitted successfully!", "success");
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
    <div className="container mt-4">
    <div className="row justify-content-center align-items-center">
      <div className="col-md-6">
        <div className="card shadow-sm">
          <div className="card-body">
            <h2 className="card-title text-center mb-3">Survey Form</h2>
            <form onSubmit={handleSubmit}>
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

              <div className="row">
                {surveyResults.map((_, index) => (
                  <div key={index} className="col-6 col-md-4 mb-3">
                    <label htmlFor={`question-${index + 1}`} className="form-label">
                      Q{index + 1}
                    </label>
                    <input
                      type="number"
                      id={`question-${index + 1}`}
                      min="1"
                      max="7"
                      value={surveyResults[index]}
                      onChange={(e) => handleResponseChange(index, Number(e.target.value))}
                      className="form-control"
                      required
                      disabled={isSubmitting}
                    />
                  </div>
                ))}
              </div>

              <div className="d-flex justify-content-between mt-3">
                <button type="submit" className="btn btn-primary btn-sm" disabled={isSubmitting}>
                  {isSubmitting ? 'Submitting...' : 'Submit Survey'}
                </button>
                <button
                  type="button"
                  onClick={handleAutoGenerateAndSubmit}
                  className="btn btn-secondary btn-sm"
                  disabled={isSubmitting}
                >
                  Auto-Fill
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>


      <div className="col-md-6">
        <div className="card h-100 overflow-auto " style={{ maxHeight: '100vh', minHeight:'100vh' }}>
          <div className="card-body">
            <h3 className="card-title text-center">Responses <span className='fs-6'>(latest 10)</span></h3>
            <div className="response-list d-flex-row justify-content-center align-items-center mt-3">
              {responses.length > 0 ? (
                responses.map((response, idx) => (
                  <div key={idx} className="card mb-3 shadow-sm">
                    <div className="card-body">
                      <h5 className="card-title">Overall Analysis: {response.overall_analysis}</h5>
                      <p className="mb-1"><strong>Animal Type:</strong> {response.cat_dog === 'dogs' ? '🐶 Dog' : '🐱 Cat'}</p>
                      <p className="mb-1"><strong>Fur Type:</strong> {response.fur_value.charAt(0).toUpperCase() + response.fur_value.slice(1)} Fur</p>
                      <p className="mb-1"><strong>Tail Length:</strong> {response.tail_value.charAt(0).toUpperCase() + response.tail_value.slice(1)}</p>

                      <h6 className="mt-3">Statistics Summary</h6>
                      <ul className="list-group list-group-flush">
                        <li className="list-group-item">Mean: {response.statistics_summary.mean}</li>
                        <li className="list-group-item">Median: {response.statistics_summary.median}</li>
                        <li className="list-group-item">Std Dev: {response.statistics_summary.standard_deviation.toFixed(2)}</li>
                      </ul>

                      <p className="mt-3"><strong>Description:</strong> {response.description}</p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-center text-muted">No Responses Yet</p>
              )}
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
  );
};

export default SurveyForm;
