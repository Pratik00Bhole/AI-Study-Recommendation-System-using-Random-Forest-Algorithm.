import { useEffect, useState } from 'react';
import api from '../services/api';
import { getUser } from '../services/auth';

const STANDARD_OPTIONS = [4, 5, 6, 7, 8, 9, 10];

const SUBJECTS_BY_STANDARD = {
  4: ['English', 'Mathematics', 'Environmental Studies', 'Hindi', 'General Knowledge'],
  5: ['English', 'Mathematics', 'Science', 'Social Studies', 'Hindi'],
  6: ['English', 'Mathematics', 'Science', 'Social Science', 'Hindi', 'Computer Basics'],
  7: ['English', 'Mathematics', 'Science', 'Social Science', 'Hindi', 'Computer Science'],
  8: ['English', 'Mathematics', 'Science', 'Social Science', 'Hindi', 'Computer Science'],
  9: ['English', 'Mathematics', 'Science', 'Social Science', 'Hindi', 'Computer Science'],
  10: ['English', 'Mathematics', 'Science', 'Social Science', 'Hindi', 'Computer Science'],
};

const LEVEL_OPTIONS = ['good', 'average', 'low'];

function ProfilePage() {
  const user = getUser();
  const initialStandard = Number(user?.standard) >= 4 && Number(user?.standard) <= 10 ? String(user.standard) : '10';

  const [studentDetails, setStudentDetails] = useState({
    full_name: user?.name || '',
    class_standard: initialStandard,
    school_name: '',
  });
  const [subjects, setSubjects] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const buildSubjectsForStandard = (standardValue, existingSubjects = []) => {
    const targetSubjects = SUBJECTS_BY_STANDARD[Number(standardValue)] || SUBJECTS_BY_STANDARD[10];
    const existingByName = existingSubjects.reduce((acc, item) => ({ ...acc, [item.name]: item }), {});
    return targetSubjects.map((name) => {
      const previous = existingByName[name];
      return {
        name,
        level: previous?.level || 'average',
        marks: previous?.marks ?? '',
      };
    });
  };

  useEffect(() => {
    setSubjects(buildSubjectsForStandard(studentDetails.class_standard));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setSubjects((previous) => buildSubjectsForStandard(studentDetails.class_standard, previous));
  }, [studentDetails.class_standard]);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const { data } = await api.get('/student/profile');
        const profile = data?.profile || {};
        if (!profile || Object.keys(profile).length === 0) {
          return;
        }

        const incomingDetails = profile.student_details || {};
        const mergedDetails = {
          full_name: incomingDetails.full_name || user?.name || '',
          class_standard: String(incomingDetails.class_standard || user?.standard || 10),
          school_name: incomingDetails.school_name || '',
        };
        setStudentDetails(mergedDetails);

        const incomingSubjects = Array.isArray(profile.subjects)
          ? profile.subjects.map((item) => ({
            name: item.name,
            level: item.level || 'average',
            marks: item.marks ?? '',
          }))
          : [];

        if (incomingSubjects.length > 0) {
          setSubjects(buildSubjectsForStandard(mergedDetails.class_standard, incomingSubjects));
        }
      } catch {
        // ignore initial load errors to keep form usable
      }
    };

    loadProfile();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleDetailChange = (key, value) => {
    setStudentDetails((previous) => ({ ...previous, [key]: value }));
  };

  const handleSubjectChange = (index, key, value) => {
    setSubjects((previous) => {
      const updated = [...previous];
      updated[index] = { ...updated[index], [key]: value };
      return updated;
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage('');
    setError('');

    const normalizedSubjects = subjects.map((subject) => {
      const marks = Number(subject.marks);
      const boundedMarks = Number.isFinite(marks) ? Math.max(0, Math.min(100, marks)) : 0;
      return {
        name: subject.name,
        level: subject.level,
        marks: boundedMarks,
      };
    });

    const marks = normalizedSubjects.reduce((acc, item) => ({ ...acc, [item.name]: item.marks }), {});
    const subjectLevels = normalizedSubjects.reduce((acc, item) => ({ ...acc, [item.name]: item.level }), {});

    const payload = {
      student_details: studentDetails,
      subjects: normalizedSubjects,
      marks,
      subject_levels: subjectLevels,
      skills: [],
      interests: [],
    };

    try {
      const { data } = await api.post('/student/profile', payload);
      setAnalysis(data.analysis);
      setMessage(data.message);
    } catch (err) {
      setError(err.userMessage || 'Unable to save profile.');
    }
  };

  return (
    <div className="card profile-page-card">
      <div className="page-header">
        <h2 className="page-title">Student Profile</h2>
        <p className="page-subtitle">Student details are shown at top. Change standard (4-10) to get subjects accordingly.</p>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="card profile-section-card">
          <h3 className="section-title">Student Profile Details</h3>
          <label>Full Name</label>
          <input
            value={studentDetails.full_name}
            onChange={(e) => handleDetailChange('full_name', e.target.value)}
            placeholder="Enter student name"
          />

          <label>Class</label>
          <select
            value={studentDetails.class_standard}
            onChange={(e) => handleDetailChange('class_standard', e.target.value)}
          >
            {STANDARD_OPTIONS.map((standard) => (
              <option key={standard} value={standard}>{standard}</option>
            ))}
          </select>

          <label>School Name</label>
          <input
            value={studentDetails.school_name}
            onChange={(e) => handleDetailChange('school_name', e.target.value)}
            placeholder="Enter school name"
          />
        </div>

        <div className="card profile-section-card">
          <h3 className="section-title">Subjects for Class {studentDetails.class_standard}</h3>
          <p className="page-subtitle profile-subtitle">Select level and enter marks for each subject.</p>

          {subjects.map((subject, index) => (
            <div key={subject.name} className="subject-row">
              <div className="subject-name">{subject.name}</div>

              <div>
                <label>Level</label>
                <select
                  value={subject.level}
                  onChange={(e) => handleSubjectChange(index, 'level', e.target.value)}
                >
                  {LEVEL_OPTIONS.map((level) => (
                    <option key={level} value={level}>
                      {level.charAt(0).toUpperCase() + level.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label>Marks</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={subject.marks}
                  onChange={(e) => handleSubjectChange(index, 'marks', e.target.value)}
                  placeholder="0-100"
                />
              </div>
            </div>
          ))}
        </div>

        <button className="btn-primary" type="submit">Save & Analyze</button>
      </form>

      {message && <p className="success">{message}</p>}
      {error && <div className="error">{error}</div>}
      {analysis && (
        <div className="grid">
          <div className="card">
            <h3>Strong Topics</h3>
            <ul className="list">
              {analysis.strong_topics.map((topic) => <li key={topic}>{topic}</li>)}
            </ul>
            {analysis.strong_topics.length === 0 && <p className="empty-state">No strong topics identified yet.</p>}
          </div>
          <div className="card">
            <h3>Weak Topics</h3>
            <ul className="list">
              {analysis.weak_topics.map((topic) => <li key={topic}>{topic}</li>)}
            </ul>
            {analysis.weak_topics.length === 0 && <p className="empty-state">No weak topics identified yet.</p>}
          </div>
        </div>
      )}
    </div>
  );
}

export default ProfilePage;
